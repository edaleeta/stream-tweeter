import moment from 'moment';

export function convertTimeStampToDateTime(timestamp) {
  let date = moment.unix(timestamp);
  return date.format("dddd, MMM D YYYY, h:mm a");
}

export function convertTimeStampToTime(timestamp) {
  let date = moment.unix(timestamp);
  return date.format("h:mm a");
} 