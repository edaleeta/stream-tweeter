import moment from 'moment';

export function convertTimeStamp(timestamp) {
  let date = moment.unix(timestamp);
  return date.format("dddd, MMMM Do YYYY, h:mm:ss a");
}