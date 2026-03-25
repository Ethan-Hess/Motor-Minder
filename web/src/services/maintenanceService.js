export function getServiceStatus(
  currentMileage,
  lastService,
  interval,
) {
  if (!interval) return 'Unknown';
  if (!lastService) return 'Overdue';

  let status = 'OK';
  const milesSince = currentMileage - lastService.mileage;

  if (interval.miles) {
    const [dueSoonMiles, overdueMiles] = interval.miles;
    if (milesSince >= overdueMiles) return 'Overdue';
    if (milesSince >= dueSoonMiles) status = 'Due Soon';
  }

  return status;
}
