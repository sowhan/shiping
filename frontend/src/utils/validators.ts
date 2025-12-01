/**
 * Form Validators
 * Client-side validation for maritime data.
 */

/**
 * Validate port code (UN/LOCODE format).
 */
export function validatePortCode(code: string): boolean {
  return /^[A-Z]{5}$/.test(code);
}

/**
 * Validate vessel dimensions.
 */
export function validateVesselDimensions(
  length: number,
  beam: number,
  draft: number
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (length <= 0 || length > 500) {
    errors.push('Length must be between 0 and 500 meters');
  }

  if (beam <= 0 || beam > 80) {
    errors.push('Beam must be between 0 and 80 meters');
  }

  if (draft <= 0 || draft > 30) {
    errors.push('Draft must be between 0 and 30 meters');
  }

  if (beam > length) {
    errors.push('Beam cannot exceed length');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate speed in knots.
 */
export function validateSpeed(speed: number): boolean {
  return speed > 0 && speed <= 40;
}

/**
 * Validate coordinates.
 */
export function validateCoordinates(lat: number, lon: number): boolean {
  return lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180;
}

/**
 * Validate IMO number.
 */
export function validateIMO(imo: string): boolean {
  if (!/^\d{7}$/.test(imo)) {
    return false;
  }

  // IMO check digit validation
  const digits = imo.split('').map(Number);
  const checkSum = digits.slice(0, 6).reduce((sum, digit, i) => sum + digit * (7 - i), 0);
  return checkSum % 10 === digits[6];
}

/**
 * Validate email address.
 */
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
