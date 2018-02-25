import moment from 'moment';

export function convertTimeStamp(timestamp) {
  let date = moment.unix(timestamp);
  return date.format("dddd, MMM D YYYY, h:mm a");
}