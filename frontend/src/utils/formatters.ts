/**
 * Data Formatters
 * Format data for display in UI.
 */

/**
 * Format distance in nautical miles.
 */
export function formatDistance(nm: number): string {
  if (nm < 1) {
    return `${Math.round(nm * 1852)} m`;
  }
  if (nm < 100) {
    return `${nm.toFixed(1)} nm`;
  }
  return `${Math.round(nm).toLocaleString()} nm`;
}

/**
 * Format duration in hours to human-readable string.
 */
export function formatDuration(hours: number): string {
  if (hours < 1) {
    return `${Math.round(hours * 60)} min`;
  }
  if (hours < 24) {
    return `${hours.toFixed(1)} hours`;
  }
  const days = Math.floor(hours / 24);
  const remainingHours = Math.round(hours % 24);
  return `${days}d ${remainingHours}h`;
}

/**
 * Format currency (USD).
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

/**
 * Format date/time.
 */
export function formatDateTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(d);
}

/**
 * Format coordinates.
 */
export function formatCoordinates(lat: number, lon: number): string {
  const latDir = lat >= 0 ? 'N' : 'S';
  const lonDir = lon >= 0 ? 'E' : 'W';
  return `${Math.abs(lat).toFixed(4)}°${latDir}, ${Math.abs(lon).toFixed(4)}°${lonDir}`;
}

/**
 * Format speed in knots.
 */
export function formatSpeed(knots: number): string {
  return `${knots.toFixed(1)} kn`;
}

/**
 * Format percentage.
 */
export function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}
