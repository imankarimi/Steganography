$(document).ready( function() {
    setImage('.cover :file', '#coverImgInp', '#cover-upload');
    setImage('.secret :file', '#secretImgInp', '#secret-upload');
});


/**************************** action methods ****************************/

function setImage(file, id, img) {
    onChangeFile(file);
    FileSelect(file);
    $(id).change(function(){readURL(this, img);});
}

function onChangeFile(file) {
    $(document).on('change', file, function () {
        var input = $(this),
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [label]);
    });
}

function FileSelect(file) {
    $(file).on('fileselect', function (event, label) {
        var input = $(this).parents('.input-group').find(':text'), log = label;
        if (input.length) {input.val(log);}
        else {if (log) alert(log);}
    });
}

function readURL(input, id) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {$(id).attr('src', e.target.result);};
        reader.readAsDataURL(input.files[0]);
    }
}