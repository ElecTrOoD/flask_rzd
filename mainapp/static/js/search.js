$.expr[":"].contains = $.expr.createPseudo(function (arg) {
    return function (elem) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});

function search(inputId, mainId, itemClass, textClass) {
    $(itemClass).show();
    let filter = $(inputId).val();
    console.log(filter)
    $(mainId).find(textClass + ":not(:contains(" + filter + "))").parents(itemClass).attr("style", "display: none !important");
}