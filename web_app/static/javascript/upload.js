// HTMLフォームから画像ファイルを選択するinput要素を取得する
var input = document.getElementById('image_file');
var form = document.getElementById('upload_form');

// ファイル選択時
$('#image_file').on('change', function(event){
    // 選択されたファイルの読み込み
    var reader = new FileReader();
    reader.onload = function(event) {
        var img = new Image();
        img.onload = function() {
            // canvasオブジェクトの生成
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            // リサイズ後の幅と高さ
            canvas.width = 300;
            canvas.height = 300;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            // リサイズした画像のURLを取得
            var dataURL = canvas.toDataURL('image/jpg');
            // URLをimg要素, id=preview の要素にセット
            $('#preview').attr('src', dataURL);
        };
        img.src = event.target.result;
    }
    reader.readAsDataURL(event.target.files[0]);
});

// 送信ボタンを押してPOSTする
form.addEventListener('submit', function(event) {
    // submitイベントをキャンセル
    event.preventDefault();
    postData('/upload', 'img_file', input);
});

// 送信
function postData(path, data_name, input_data) {
    // 選択された画像ファイルを取得
    var file = input_data.files[0];

    // FormDataオブジェクトを生成し
    // フォームデータに画像ファイルを追加する
    var formData = new FormData();
    formData.append(data_name, file);

    // Ajaxリクエストを作成
    var xhr = new XMLHttpRequest();
    xhr.open('POST', path);
    xhr.send(formData);

    // レスポンスの内容を表示
    xhr.onload = function() {
       $('#log').text(xhr.responseText);
    };
}