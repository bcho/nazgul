function convertDatetime(field) {
  return (x) => {
    x[field] = new Date(x[field]);
  };
}

function datetimeToDate(dt) {
  return `${dt.getFullYear()}-${dt.getMonth() + 1}-${dt.getDate()}`;
}
