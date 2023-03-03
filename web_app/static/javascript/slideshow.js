var img_array = new Array();
var slideshow = document.getElementById("slideshow");
var next = document.getElementById("next");
var back = document.getElementById("back");
// 表示する画像番号
var count = 0;

window.onload = function() {    
    getFile('/get_img');
    next.addEventListener('click', next_img);
    back.addEventListener('click', back_img);  
};

// ファイルを取得する
function getFile(url) {
    // GETリクエストの作成
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    // xhr.readystateが変化したときに実行
    xhr.onreadystatechange = function() {
        // xhr.readystateが変化したときに実行にしているため、
        // statusが200かつstateが4のときのみ実行するようにする
        // stateは 2 -> 3 -> 4と変化する
        if (xhr.status == 200 && xhr.readyState === 4) {
            files = JSON.parse(xhr.responseText);
            var container = document.getElementById('img_container');
            
            for (var i = 0; i < files.length; i += 1) {
                var img = new Image();
                img_path = '/static/images/' + files[i];
                img_array[i] = img_path;
                img.src = img_path;
                //container.appendChild(img);
            }
            // 取得が終わったら1枚目の画像を表示する
            change();
        }
    };
    // GETリクエストを送信
    xhr.send(null);
}

function change() {
    slideshow.src = img_array[count];
}

function next_img() {
    if (count === img_array.length - 1) {
        count = 0;
    } else {
        count += 1;
    }
    change();
}

function back_img() {
    if (count === 0) {
        count = img_array.length - 1;
    } else {
        count -= 1;
    }
    change();
}
