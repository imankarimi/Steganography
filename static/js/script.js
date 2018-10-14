$(document).ready( function() {
    setImage('.cover :file', '#coverImgInp', '#cover-upload');
    setImage('.secret :file', '#secretImgInp', '#secret-upload');

    $('#stegano_encode').on('submit', (function (e) {
        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                if(data['valid'] === true){
                    console.log("success");
                    var body = '<img src="/'+data['encode_image']+'" width="100%">';
                    $('#encode_model').find('.modal-body').append(body);
                    $('#encode_model').find('.modal-footer').find('a').attr('href', "/"+data['encode_image']);
                    $('#encode_model').find('.modal-footer').find('a').attr('download', data['name']);
                    $('#show_image').click();
                }else{
                    console.log("error");
                }
            },
            error: function(){
                console.log("error");
            }
        });
    }));
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