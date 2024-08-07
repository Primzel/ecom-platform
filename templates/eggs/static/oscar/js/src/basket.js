function addToBasketFormHandler(form) {
    var selected = [];
    $($(form).serializeArray()).each(function (index, field) {
        if (['quantity', 'csrfmiddlewaretoken'].indexOf(field['name']) == -1) {
            selected.push(field['value'].split(','));
        }
    });
    var selected_child = _.intersection(...selected);
    if (selected_child) {
        selected_child = selected_child[0];
        $(form).attr('action', '/basket/add/' + selected_child + '/');
        return true;
    }
    return false;
}