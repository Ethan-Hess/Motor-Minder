import { SERVICE_STATUS } from '../types/domain.js';

export function getServiceStatus(
  currentMileage,
  lastService,
  interval,
) {
  if (!interval) return SERVICE_STATUS.UNKNOWN;
  if (!lastService) return SERVICE_STATUS.OVERDUE;

  let status = SERVICE_STATUS.OK;
  const milesSince = currentMileage - lastService.mileage;

  if (interval.miles) {
    const [dueSoonMiles, overdueMiles] = interval.miles;
    if (milesSince >= overdueMiles) return SERVICE_STATUS.OVERDUE;
    if (milesSince >= dueSoonMiles) status = SERVICE_STATUS.DUE_SOON;
  }

  return status;
}
