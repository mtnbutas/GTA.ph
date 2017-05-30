$(window).resize(function () {
    location.reload();
});
CKEDITOR.on('instanceLoaded', function(e) {e.editor.resize($('#form').width(), 450)} );
CKEDITOR.autogrow = true;
CKEDITOR.extraPlugins = 'uploadimage';
function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$('input[type="file"]').change(function(){
    readURL(this);
});