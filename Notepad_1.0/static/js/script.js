
//content head 클릭시 contentbody 접고 열기
const contentHeads = document.querySelectorAll('.content-head');
contentHeads.forEach(head => {
    head.addEventListener('click', function () {

        if (event.target.closest('.button-group')) {
            return;
        }
        const body = this.nextElementSibling;
        if (body.style.display === 'none') {
            body.style.display = 'block';
        } else {
            body.style.display = 'none';
        }
    });
});

// 동그라미 색상 변경
const circles = document.querySelectorAll('.content > .content-head > .content-head-left > .content-head-title > .status');
const textInputs = document.querySelectorAll('.content > .content-body[contenteditable]');

//content-body 내용이 입력중일때
textInputs.forEach((textInput, index) => {
    textInput.addEventListener('input', function () {
        // 해당 인덱스의 동그라미를 주황색으로 변경
        circles[index].style.backgroundColor = 'orange';

    });
});

//새로 만든 + 누를때 생기는 addtitle
const plusButtons = document.querySelectorAll('.plus input[type="button"]');
plusButtons.forEach(plusButton => {
    plusButton.addEventListener('click', function () {
        const newli = document.createElement('li');
        newli.className = 'add-content';

        const newForm = document.createElement('form');
        newForm.method = 'POST';
        newForm.action = '/create/';

        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = 'content-title';

        const newButton = document.createElement('input');
        newButton.type = 'submit';
        newButton.value = '저장';

        const hiddenTitleInput = document.createElement('input');
        hiddenTitleInput.type = 'hidden';
        hiddenTitleInput.name = 'chapter-title';
        hiddenTitleInput.value = this.parentElement.parentElement.firstElementChild.querySelector('h1').innerText;

        newForm.appendChild(newInput);
        newForm.appendChild(newButton);
        newForm.appendChild(hiddenTitleInput);
        newli.appendChild(newForm)

        // + 버튼 숨기기
        this.style.display = 'none';
        this.parentNode.insertBefore(newli, this);

        //스크롤 위치 저장
        saveScrollPosition();

    });
});


//content 저장
function save_content(form) {
    //id값을 hidden[id]에 넣기
    form.querySelector('input[name="id"]').value = form.parentElement.parentElement.querySelector('.id').innerText;

    //content [content]에 넣기
    form.querySelector('input[name="content"]').value = form.parentElement.parentElement.nextElementSibling.innerHTML;

    //스크롤 위치 저장
    //saveScrollPosition();

}

//content 종결
function close_content(form) {
    //id값을 hidden[id]에 넣기
    form.querySelector('input[name="id"]').value = form.parentElement.parentElement.querySelector('.id').innerText;

    //스크롤 위치 저장
    saveScrollPosition();

    // status 빨간색으로 하는 거 근데 이게 빨간색이 유지가 안되네.. 파이썬으로 종결할때 빨갛게 해야겠다. 짜피 종결할때말고 빨간색 안바꿈
    form.parentElement.parentElement.querySelector('.status').style.backgroundColor = 'red';


}

//content 삭제
function delete_content(form) {
    //id값을 hidden[id]에 넣기
    form.querySelector('input[name="id"]').value = form.parentElement.parentElement.querySelector('.id').innerText;

    //스크롤 위치 저장
    saveScrollPosition();

}

//ctrl + s 누르면 저장
document.addEventListener("keydown", function (e) {

    // Ctrl + S (또는 Command + S on Mac)를 눌렀을 때
    if ((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey) && e.key === 's') {

        // 기본 동작 방지 (페이지 저장)
        e.preventDefault();

        saveScrollPosition()

        // 현재 포커스된 contenteditable div 확인
        var focusedDiv = document.activeElement;

        // save 버튼 찾기
        var container = focusedDiv.closest('.content');
        var saveButton = container.querySelector('.button-group form input[type="submit"][value="저장"]');

        // 버튼 클릭
        saveButton.click();
    }
});

//스크롤 유지
// 스크롤 위치 저장
function saveScrollPosition() {
    document.cookie = "scrollPosition=" + window.scrollY + "; path=/";
}

// 페이지 로드 시 
window.onload = function () {
    //스크롤 위치 복원
    restoreScrollPosition();

    //circle 빨간색이면 block
    circles.forEach(circle => {
        const contentBody = circle.closest('.content-head').nextElementSibling;

        //circle 요소의 실제 스타일 가져오기
        const computedStyle = window.getComputedStyle(circle);

        if (computedStyle.backgroundColor === 'rgb(255, 0, 0)') {
            contentBody.style.display = 'none';
        } else {
            contentBody.style.display = 'block';
        }
    });
};


// 스크롤 위치 복원
function restoreScrollPosition() {
    const match = document.cookie.match(/scrollPosition=(\d+)/);
    if (match) {
        window.scrollTo(0, parseInt(match[1], 10));
    }
}
//F5 키 누르면 홈으로 이동
document.addEventListener('keydown', function (event) {
    if (event.key === 'F5') {
        event.preventDefault(); // 기본 F5 동작을 차단합니다.
        saveScrollPosition();
        window.location.href = '/'; // 홈 페이지로 리다이렉트합니다.
        restoreScrollPosition();
    }
});


