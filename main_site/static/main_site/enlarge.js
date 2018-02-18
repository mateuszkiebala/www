// Copyright [c] 2005 Mikrobit Sp. z o.o.. All Rights Reserved.
function enlarge(sAdres) {
if (sAdres.indexOf('png') != -1) {
iWidth = 774;
iHeight = 675;
} else {
iWidth = screen.width < 1024 ? screen.width : 1024;
iHeight = 740;
}
var nW = window.open(sAdres, "", "left=0,top=0,toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=0,width=" + iWidth + ",height=" + iHeight);
nW.document.title.value = 'Wybory 2005';
}