import moment from 'moment';
import 'moment-timezone';

export function convertTimeStampToDateTime(timestamp) {
  let date = moment.unix(timestamp);
  return date.format("dddd, MMM D YYYY, h:mm a");
}

export function convertTimeStampToTime(timestamp) {
  let date = moment.unix(timestamp);
  return date.format("h:mm a");
} 

export function roundTimeToMinute(timestamp) {
  let date = moment.unix(timestamp);
  let roundDownMinute = date.startOf('minute');
  return roundDownMinute.unix();
}

export function convertToCommaSeparated(num) {
  return num.toLocaleString('en')
}

export function convertTimeStampToTimeAndTZ (timestamp) {
  timestamp = convertTimeStampToTime(timestamp)
  let user_tz = moment().tz(moment.tz.guess()).format('z');
  return timestamp.toUpperCase() + " " + user_tz;
}