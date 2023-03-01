// HTMLフォームから画像ファイルを選択するinput要素を取得する
var input = document.getElementById('image_file');
var form = document.getElementById('upload_form');

$('#image_file').on('change', function(event){
    var reader = new FileReader();
    reader.onload = function(event) {
        var img = new Image();
        img.onload = function() {
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            // リサイズ後の幅と高さ
            canvas.width = 300;
            canvas.height = 300;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            // リサイズした画像のURLを取得
            var dataURL = canvas.toDataURL('image/jpg');
            $('#preview').attr('src', dataURL);
        };
        img.src = event.target.result;
    }
    reader.readAsDataURL(event.target.files[0]);
});

// input要素のchangeイベントを監視
// ファイルが選択されたら、処理を開始する
/*
input.addEventListener('change', function(){
    postData();
});
*/

// 送信ボタンを押してPOSTする
form.addEventListener('submit', function(event) {
    // submitイベントをキャンセル
    event.preventDefault();
    postData();
});

// 送信
function postData() {
    // 選択された画像ファイルを取得
    var file = input.files[0];
    var log = document.getElementById('log');
    log.textContent = 'submit';

    // FormDataオブジェクトを生成し
    // フォームデータに画像ファイルを追加する
    var formData = new FormData();
    formData.append('image_file', file);

    // Ajaxリクエストを作成
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload');
    xhr.send(formData);

    // レスポンスの内容を表示
    xhr.onload = function() {
        console.log(xhr.responseText);
    };
}