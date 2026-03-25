export const SERVICE_NAMES = [
  'oil_change',
  'air_intake_filter',
  'cabin_air_filter',
  'tire_rotation',
  'transmission_fluid',
  'brake_pads_inspection',
  'battery',
  'coolant_flush',
  'spark_plugs',
  'brake_fluid',
];

const SERVICE_NAME_SET = new Set(SERVICE_NAMES);

export const SERVICE_STATUS = Object.freeze({
  OK: 'OK',
  DUE_SOON: 'Due Soon',
  OVERDUE: 'Overdue',
  UNKNOWN: 'Unknown',
});

export function isKnownServiceName(serviceName) {
  return SERVICE_NAME_SET.has(serviceName);
}

export function createServiceRecord(input = {}) {
  const mileage = Number.isFinite(input.mileage)
    ? input.mileage
    : Number.parseInt(input.mileage ?? 0, 10);

  return {
    mileage: Number.isFinite(mileage) ? mileage : 0,
    date: typeof input.date === 'string' ? input.date : '',
  };
}

export function normalizeLastService(lastService = {}) {
  const normalized = {};

  Object.entries(lastService).forEach(([serviceName, record]) => {
    if (!isKnownServiceName(serviceName)) {
      return;
    }

    normalized[serviceName] = createServiceRecord(record);
  });

  return normalized;
}

export function createVehicle(input = {}) {
  const currentMileage = Number.isFinite(input.currentMileage)
    ? input.currentMileage
    : Number.parseInt(input.currentMileage ?? input.current_mileage ?? 0, 10);

  return {
    id: typeof input.id === 'string' ? input.id : '',
    userId: typeof input.userId === 'string' ? input.userId : '',
    make: typeof input.make === 'string' ? input.make : '',
    model: typeof input.model === 'string' ? input.model : '',
    year: Number.isFinite(input.year) ? input.year : Number.parseInt(input.year ?? 0, 10),
    currentMileage: Number.isFinite(currentMileage) ? currentMileage : 0,
    lastService: normalizeLastService(input.lastService ?? input.last_service ?? {}),
  };
}

export function toWebVehicleFromMvp(mvpVehicle, options = {}) {
  return createVehicle({
    id: options.id ?? '',
    userId: options.userId ?? '',
    make: mvpVehicle?.make,
    model: mvpVehicle?.model,
    year: mvpVehicle?.year,
    current_mileage: mvpVehicle?.current_mileage,
    last_service: mvpVehicle?.last_service,
  });
}

export function toMvpVehicleFromWeb(webVehicle) {
  const vehicle = createVehicle(webVehicle);

  return {
    make: vehicle.make,
    model: vehicle.model,
    year: vehicle.year,
    current_mileage: vehicle.currentMileage,
    last_service: vehicle.lastService,
  };
}

export function createAddress(input = {}) {
  return {
    address_line_1: typeof input.address_line_1 === 'string' ? input.address_line_1 : '',
    address_line_2: typeof input.address_line_2 === 'string' ? input.address_line_2 : '',
    city: typeof input.city === 'string' ? input.city : '',
    state: typeof input.state === 'string' ? input.state : '',
    zip_code: Number.isFinite(input.zip_code) ? input.zip_code : Number.parseInt(input.zip_code ?? 0, 10),
    country: typeof input.country === 'string' ? input.country : '',
  };
}

export function createMechanic(input = {}) {
  return {
    name: typeof input.name === 'string' ? input.name : '',
    address: createAddress(input.address),
    phone: typeof input.phone === 'string' ? input.phone : '',
    email: typeof input.email === 'string' ? input.email : '',
    website: typeof input.website === 'string' ? input.website : '',
    services: Array.isArray(input.services) ? input.services.filter(isKnownServiceName) : [],
    rating: Number.isFinite(input.rating) ? input.rating : Number.parseFloat(input.rating ?? 0),
    price_range: typeof input.price_range === 'string' ? input.price_range : '$',
    appointment_required: Boolean(input.appointment_required),
    hours: input.hours && typeof input.hours === 'object' ? input.hours : {},
  };
}
