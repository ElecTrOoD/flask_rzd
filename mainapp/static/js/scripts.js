function normalize_date(date) {
    let date_options = {
        day: 'numeric',
        month: 'numeric',
        year: '2-digit',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
    };
    let new_date = new Date(Date.parse(date))
    return new_date.toLocaleString('ru', date_options)
}