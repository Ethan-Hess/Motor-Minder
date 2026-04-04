import { SERVICE_STATUS } from '../types/domain.js';

const DAY_IN_MS = 24 * 60 * 60 * 1000;

function parseIsoDate(dateString) {
  if (typeof dateString !== 'string') {
    return null;
  }

  const [yearRaw, monthRaw, dayRaw] = dateString.split('-');
  const year = Number.parseInt(yearRaw, 10);
  const month = Number.parseInt(monthRaw, 10);
  const day = Number.parseInt(dayRaw, 10);

  if (!Number.isInteger(year) || !Number.isInteger(month) || !Number.isInteger(day)) {
    return null;
  }

  return new Date(Date.UTC(year, month - 1, day));
}

function formatIsoDate(dateValue) {
  return dateValue.toISOString().slice(0, 10);
}

function normalizeDateInput(dateInput) {
  if (!dateInput) {
    return new Date();
  }

  if (dateInput instanceof Date) {
    return dateInput;
  }

  const parsed = parseIsoDate(dateInput);
  return parsed ?? new Date();
}

function getDaysInMonthUtc(year, monthIndex) {
  return new Date(Date.UTC(year, monthIndex + 1, 0)).getUTCDate();
}

function addMonthsCalendarAware(dateValue, monthsToAdd) {
  const year = dateValue.getUTCFullYear();
  const month = dateValue.getUTCMonth();
  const day = dateValue.getUTCDate();
  const absoluteTargetMonth = month + monthsToAdd;
  const targetYear = year + Math.floor(absoluteTargetMonth / 12);
  const targetMonth = ((absoluteTargetMonth % 12) + 12) % 12;
  const maxDay = getDaysInMonthUtc(targetYear, targetMonth);
  const targetDay = Math.min(day, maxDay);

  return new Date(Date.UTC(targetYear, targetMonth, targetDay));
}

function addYearsCalendarAware(dateValue, yearsToAdd) {
  return addMonthsCalendarAware(dateValue, yearsToAdd * 12);
}

function fullMonthsBetween(startDate, endDate) {
  let months = (endDate.getUTCFullYear() - startDate.getUTCFullYear()) * 12;
  months += endDate.getUTCMonth() - startDate.getUTCMonth();

  if (endDate.getUTCDate() < startDate.getUTCDate()) {
    months -= 1;
  }

  return months;
}

function fullYearsBetween(startDate, endDate) {
  let years = endDate.getUTCFullYear() - startDate.getUTCFullYear();
  const endMonth = endDate.getUTCMonth();
  const startMonth = startDate.getUTCMonth();

  if (endMonth < startMonth || (endMonth === startMonth && endDate.getUTCDate() < startDate.getUTCDate())) {
    years -= 1;
  }

  return years;
}

function daysOverdue(todayDate, dueDate) {
  const utcToday = Date.UTC(todayDate.getUTCFullYear(), todayDate.getUTCMonth(), todayDate.getUTCDate());
  const utcDue = Date.UTC(dueDate.getUTCFullYear(), dueDate.getUTCMonth(), dueDate.getUTCDate());

  return Math.floor((utcToday - utcDue) / DAY_IN_MS);
}

function appendOverdueAmount(currentOverdueAmount, suffix) {
  if (!suffix) {
    return currentOverdueAmount;
  }

  if (!currentOverdueAmount) {
    return suffix;
  }

  return `${currentOverdueAmount}, ${suffix}`;
}

export function getServiceStatusDetailed(currentMileage, lastService, interval, today) {
  if (!interval) {
    return {
      status: SERVICE_STATUS.UNKNOWN,
      dueMiles: null,
      dueDate: null,
      overdueAmount: null,
      missing: true,
    };
  }

  if (!lastService) {
    return {
      status: SERVICE_STATUS.OVERDUE,
      dueMiles: null,
      dueDate: null,
      overdueAmount: null,
      missing: true,
    };
  }

  const mileageNow = Number.isFinite(currentMileage)
    ? currentMileage
    : Number.parseInt(currentMileage ?? 0, 10);

  const lastMileage = Number.isFinite(lastService.mileage)
    ? lastService.mileage
    : Number.parseInt(lastService.mileage ?? 0, 10);

  const todayDate = normalizeDateInput(today);
  const lastServiceDate = parseIsoDate(lastService.date);

  let status = SERVICE_STATUS.OK;
  let dueMiles = null;
  let dueDate = null;
  let overdueAmount = null;

  if (interval.miles) {
    const [dueSoonMiles, overdueMiles] = interval.miles;
    const milesSince = mileageNow - lastMileage;
    dueMiles = lastMileage + overdueMiles;

    if (milesSince >= overdueMiles) {
      status = SERVICE_STATUS.OVERDUE;

      if (mileageNow > dueMiles) {
        overdueAmount = `${mileageNow - dueMiles} mi over`;
      }
    } else if (milesSince >= dueSoonMiles) {
      status = SERVICE_STATUS.DUE_SOON;
    }
  }

  if (lastServiceDate && interval.months) {
    const [dueSoonMonths, overdueMonths] = interval.months;
    const elapsedMonths = fullMonthsBetween(lastServiceDate, todayDate);
    const maxDueDate = addMonthsCalendarAware(lastServiceDate, overdueMonths);
    dueDate = formatIsoDate(maxDueDate);

    if (elapsedMonths >= overdueMonths) {
      status = SERVICE_STATUS.OVERDUE;
      const overdueDays = daysOverdue(todayDate, maxDueDate);

      if (overdueDays > 0) {
        overdueAmount = appendOverdueAmount(overdueAmount, `${overdueDays} days over`);
      }
    } else if (status !== SERVICE_STATUS.OVERDUE && elapsedMonths >= dueSoonMonths) {
      status = SERVICE_STATUS.DUE_SOON;
    }
  }

  if (lastServiceDate && interval.years) {
    const [dueSoonYears, overdueYears] = interval.years;
    const elapsedYears = fullYearsBetween(lastServiceDate, todayDate);
    const maxDueDate = addYearsCalendarAware(lastServiceDate, overdueYears);
    dueDate = formatIsoDate(maxDueDate);

    if (elapsedYears >= overdueYears) {
      status = SERVICE_STATUS.OVERDUE;
      const overdueDays = daysOverdue(todayDate, maxDueDate);

      if (overdueDays > 0) {
        overdueAmount = appendOverdueAmount(overdueAmount, `${overdueDays} days over`);
      }
    } else if (status !== SERVICE_STATUS.OVERDUE && elapsedYears >= dueSoonYears) {
      status = SERVICE_STATUS.DUE_SOON;
    }
  }

  return {
    status,
    dueMiles,
    dueDate,
    overdueAmount,
    missing: false,
  };
}

export function getServiceStatus(
  currentMileage,
  lastService,
  interval,
  today,
) {
  return getServiceStatusDetailed(currentMileage, lastService, interval, today).status;
}
