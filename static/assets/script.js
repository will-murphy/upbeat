/*
|--------------------------------------------------------------------------
| ADMIN CONFIGS
|--------------------------------------------------------------------------
*/
window.specialusers = [
    'jstep',
    'orleanspobee',
    'garysheng',
    'mattpiccolella',
    'sghelm',
    'ericahalp',
    'zlawrence',
    'sundeepk',
    'caseyhuang',
    'rzendacott',
    'bitbanger',
    'hsubrama',
    'kevinlei',
    'vbracht',
    'pravallikat',
    'charjmays',
    'matthewo',
    'danlee',
    'binfu',
    'deniskov',
    'pomeroy',
    'dhp',
    'mhathorn',
    'eustace',
    'urs',
    'omridor',
    'scmcfetridge',
    'phinkle',
    'rgevertz'
];
function isspecial(user){
    return window.specialusers.indexOf(user) !== -1;
}
function imspecial(){
    return isspecial(window.inuser);
}

window.titlepreserved = document.title;

//firefox gets special treatment because it doesn't work as well as chrome
var is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;

/*
|--------------------------------------------------------------------------
| TOOL STUFF
|--------------------------------------------------------------------------
*/
var hasClass = function (elem, className) {
    return new RegExp(' ' + className + ' ').test(' ' + elem.className + ' ');
}
var addClass = function (elem, className) {
    if (!hasClass(elem, className)) {
        elem.className += ' ' + className;
    }
}
var toggleClass = function (el, className) {
    el.classList.toggle(className);
 //  if(el) {
 //    if(el.className.indexOf(className)) {
 //      el.className = el.className.replace(className, '');
 //    }

 //    else {
 //      el.className += ' ' + className;
 //    }
 // }
}
var removeClass = function (elem, className) {
    var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ') + ' ';
    if (hasClass(elem, className)) {
        while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
            newClass = newClass.replace(' ' + className + ' ', ' ');
        }
        elem.className = newClass.replace(/^\s+|\s+$/g, '');
    }
}
function closest(el, tagname) {
    var fn = function (el) {
        if(!el.tagName){
            return true;
        }
        return el.tagName.toLowerCase() === tagname;
    }
    return el && (
        fn(el) ? el : closest(el.parentNode, fn)
    );
}
function closestId(el, id) {
    if(el.hasAttribute('id') && el.getAttribute('id') == id){
        return el;
    }
    return closestId(el.parentNode, id);
}
function capThatFirstLetter(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function timeago(mom){
    var difference = moment.utc() - mom;
    difference = Math.round(difference/1000);

    if(difference < 60){
        return 'just now';
    }else if(difference < 60*2){
        return '1 min ago';
    }else if(difference < 60*60){
        return Math.floor(difference/60) + ' mins ago';
    }else if(difference < 60*60*2){
        return '1 hour ago';
    }else if(difference < 60*60*24){
        return Math.floor(difference/60/60) + ' hours ago';
    }else if(difference < 60*60*24*2){
        return 'yesterday';
    }else if(difference < 60*60*24*7){
        return Math.floor(difference/60/60/24) + ' days ago';
    }else if(difference < 60*60*24*7*2){
        return 'last week';
    }else if(difference < 60*60*24*7*3){
        return '2 weeks ago';
    }else{
        var local = mom.local();

        var months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
        var month = months[mom.month()];

        var day = mom.day()+1;

        if(moment().year() == local.year()){
            return month+' '+day;
        //show year
        }else{
            return month+' '+day+', '+mom.year();
        }
    }
}
function linkify(string) {
    string = string.replace(/((http|https|ftp)\:\/\/|\bw{3}\.)[a-z0-9\-\.]+\.[a-z]{2,3}(:[a-z0-9]*)?\/?([a-z\u00C0-\u017F0-9\-\._\?\,\'\/\\\+&amp;%\$#\=~])*/gi, function(captured) {
        var uri;
        if (captured.toLowerCase().indexOf("www.") == 0) {
            uri = "http://" + captured;
        } else {
            uri = captured;
        }
        var alteredcaptured = captured.length > 30 ? captured.substring(0, 27)+'...' : captured;
        return "<a href=\"" + uri+ "\" target=\"_blank\"" + ">" + alteredcaptured + "</a>";
    });

    string = string.replace(/go\/[^\s]+/gi, function(captured) {
        var uri;
        if(captured.indexOf('go/') != 0){
            return captured;
        }
        uri = 'http://goto.google.com/'+captured.substring(3);
        return "<a href=\"" + uri+ "\" target=\"_blank\"" + ">" + captured + "</a>";
    });

    function atUrl(at) {
        return "/user/" + at;
    }
    string = string.replace(/\B@(\w+)/g, "<a href=" + atUrl("$1") +" target=\"_blank\"" + ">@$1</a>");

    if (false) {
        string = string.replace(/\B#(\w+)/g, "<a href=" + buildHashtagUrl("$1") +" target=\"_blank\"" + ">#$1</a>");
    }
    return string;
}
function htmlEscape(str) {
    return String(str)
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(' ', '&nbsp;');
}
function stuffEncode(text){
    var result = htmlEscape(text);
    result = linkify(result);
    result = result.replace(/(?:\r\n|\r|\n)/g, '<br>');
    return result;
}
function linkFilter(url){
    url = url.trim();
    if(url.indexOf('go/') === 0){
        url = url.substring(3);
        url = 'http://goto.google.com/'+url;
    }
    if(url.indexOf('http') !== 0){
        url = 'http://'+url;
    }
    return url;
}
function prepend(child, parent){
    parent.insertBefore(child,parent.firstChild);
}
function objectToFormdata(obj){
    var formdata = new FormData();
    for(var name in obj){
        formdata.append(name, obj[name]);
    }
    return formdata;
}

// console.log('%cSCROOGLED!', 'font-size:56px;text-shadow: -1px -1px hsl(0,100%,50%), 1px 1px hsl(5.4, 100%, 50%), 3px 2px hsl(10.8, 100%, 50%), 5px 3px hsl(16.2, 100%, 50%), 7px 4px hsl(21.6, 100%, 50%), 9px 5px hsl(27, 100%, 50%), 11px 6px hsl(32.4, 100%, 50%), 13px 7px hsl(37.8, 100%, 50%), 14px 8px hsl(43.2, 100%, 50%), 16px 9px hsl(48.6, 100%, 50%), 18px 10px hsl(54, 100%, 50%), 20px 11px hsl(59.4, 100%, 50%), 22px 12px hsl(64.8, 100%, 50%), 23px 13px hsl(70.2, 100%, 50%), 25px 14px hsl(75.6, 100%, 50%), 27px 15px hsl(81, 100%, 50%), 28px 16px hsl(86.4, 100%, 50%), 30px 17px hsl(91.8, 100%, 50%), 32px 18px hsl(97.2, 100%, 50%), 33px 19px hsl(102.6, 100%, 50%), 35px 20px hsl(108, 100%, 50%), 36px 21px hsl(113.4, 100%, 50%), 38px 22px hsl(118.8, 100%, 50%), 39px 23px hsl(124.2, 100%, 50%), 41px 24px hsl(129.6, 100%, 50%), 42px 25px hsl(135, 100%, 50%), 43px 26px hsl(140.4, 100%, 50%), 45px 27px hsl(145.8, 100%, 50%), 46px 28px hsl(151.2, 100%, 50%), 47px 29px hsl(156.6, 100%, 50%), 48px 30px hsl(162, 100%, 50%), 49px 31px hsl(167.4, 100%, 50%), 50px 32px hsl(172.8, 100%, 50%), 51px 33px hsl(178.2, 100%, 50%), 52px 34px hsl(183.6, 100%, 50%), 53px 35px hsl(189, 100%, 50%), 54px 36px hsl(194.4, 100%, 50%), 55px 37px hsl(199.8, 100%, 50%), 55px 38px hsl(205.2, 100%, 50%), 56px 39px hsl(210.6, 100%, 50%), 57px 40px hsl(216, 100%, 50%), 57px 41px hsl(221.4, 100%, 50%), 58px 42px hsl(226.8, 100%, 50%), 58px 43px hsl(232.2, 100%, 50%), 58px 44px hsl(237.6, 100%, 50%), 59px 45px hsl(243, 100%, 50%), 59px 46px hsl(248.4, 100%, 50%), 59px 47px hsl(253.8, 100%, 50%), 59px 48px hsl(259.2, 100%, 50%), 59px 49px hsl(264.6, 100%, 50%), 60px 50px hsl(270, 100%, 50%), 59px 51px hsl(275.4, 100%, 50%), 59px 52px hsl(280.8, 100%, 50%), 59px 53px hsl(286.2, 100%, 50%), 59px 54px hsl(291.6, 100%, 50%), 59px 55px hsl(297, 100%, 50%), 58px 56px hsl(302.4, 100%, 50%), 58px 57px hsl(307.8, 100%, 50%), 58px 58px hsl(313.2, 100%, 50%), 57px 59px hsl(318.6, 100%, 50%), 57px 60px hsl(324, 100%, 50%), 56px 61px hsl(329.4, 100%, 50%), 55px 62px hsl(334.8, 100%, 50%), 55px 63px hsl(340.2, 100%, 50%), 54px 64px hsl(345.6, 100%, 50%), 53px 65px hsl(351, 100%, 50%), 52px 66px hsl(356.4, 100%, 50%), 51px 67px hsl(361.8, 100%, 50%), 50px 68px hsl(367.2, 100%, 50%), 49px 69px hsl(372.6, 100%, 50%), 48px 70px hsl(378, 100%, 50%), 47px 71px hsl(383.4, 100%, 50%), 46px 72px hsl(388.8, 100%, 50%), 45px 73px hsl(394.2, 100%, 50%), 43px 74px hsl(399.6, 100%, 50%), 42px 75px hsl(405, 100%, 50%), 41px 76px hsl(410.4, 100%, 50%), 39px 77px hsl(415.8, 100%, 50%), 38px 78px hsl(421.2, 100%, 50%), 36px 79px hsl(426.6, 100%, 50%), 35px 80px hsl(432, 100%, 50%), 33px 81px hsl(437.4, 100%, 50%), 32px 82px hsl(442.8, 100%, 50%), 30px 83px hsl(448.2, 100%, 50%), 28px 84px hsl(453.6, 100%, 50%), 27px 85px hsl(459, 100%, 50%), 25px 86px hsl(464.4, 100%, 50%), 23px 87px hsl(469.8, 100%, 50%), 22px 88px hsl(475.2, 100%, 50%), 20px 89px hsl(480.6, 100%, 50%), 18px 90px hsl(486, 100%, 50%), 16px 91px hsl(491.4, 100%, 50%), 14px 92px hsl(496.8, 100%, 50%), 13px 93px hsl(502.2, 100%, 50%), 11px 94px hsl(507.6, 100%, 50%), 9px 95px hsl(513, 100%, 50%), 7px 96px hsl(518.4, 100%, 50%), 5px 97px hsl(523.8, 100%, 50%), 3px 98px hsl(529.2, 100%, 50%), 1px 99px hsl(534.6, 100%, 50%), 7px 100px hsl(540, 100%, 50%), -1px 101px hsl(545.4, 100%, 50%), -3px 102px hsl(550.8, 100%, 50%), -5px 103px hsl(556.2, 100%, 50%), -7px 104px hsl(561.6, 100%, 50%), -9px 105px hsl(567, 100%, 50%), -11px 106px hsl(572.4, 100%, 50%), -13px 107px hsl(577.8, 100%, 50%), -14px 108px hsl(583.2, 100%, 50%), -16px 109px hsl(588.6, 100%, 50%), -18px 110px hsl(594, 100%, 50%), -20px 111px hsl(599.4, 100%, 50%), -22px 112px hsl(604.8, 100%, 50%), -23px 113px hsl(610.2, 100%, 50%), -25px 114px hsl(615.6, 100%, 50%), -27px 115px hsl(621, 100%, 50%), -28px 116px hsl(626.4, 100%, 50%), -30px 117px hsl(631.8, 100%, 50%), -32px 118px hsl(637.2, 100%, 50%), -33px 119px hsl(642.6, 100%, 50%), -35px 120px hsl(648, 100%, 50%), -36px 121px hsl(653.4, 100%, 50%), -38px 122px hsl(658.8, 100%, 50%), -39px 123px hsl(664.2, 100%, 50%), -41px 124px hsl(669.6, 100%, 50%), -42px 125px hsl(675, 100%, 50%), -43px 126px hsl(680.4, 100%, 50%), -45px 127px hsl(685.8, 100%, 50%), -46px 128px hsl(691.2, 100%, 50%), -47px 129px hsl(696.6, 100%, 50%), -48px 130px hsl(702, 100%, 50%), -49px 131px hsl(707.4, 100%, 50%), -50px 132px hsl(712.8, 100%, 50%), -51px 133px hsl(718.2, 100%, 50%), -52px 134px hsl(723.6, 100%, 50%), -53px 135px hsl(729, 100%, 50%), -54px 136px hsl(734.4, 100%, 50%), -55px 137px hsl(739.8, 100%, 50%), -55px 138px hsl(745.2, 100%, 50%), -56px 139px hsl(750.6, 100%, 50%), -57px 140px hsl(756, 100%, 50%), -57px 141px hsl(761.4, 100%, 50%), -58px 142px hsl(766.8, 100%, 50%), -58px 143px hsl(772.2, 100%, 50%), -58px 144px hsl(777.6, 100%, 50%), -59px 145px hsl(783, 100%, 50%), -59px 146px hsl(788.4, 100%, 50%), -59px 147px hsl(793.8, 100%, 50%), -59px 148px hsl(799.2, 100%, 50%), -59px 149px hsl(804.6, 100%, 50%), -60px 150px hsl(810, 100%, 50%), -59px 151px hsl(815.4, 100%, 50%), -59px 152px hsl(820.8, 100%, 50%), -59px 153px hsl(826.2, 100%, 50%), -59px 154px hsl(831.6, 100%, 50%), -59px 155px hsl(837, 100%, 50%), -58px 156px hsl(842.4, 100%, 50%), -58px 157px hsl(847.8, 100%, 50%), -58px 158px hsl(853.2, 100%, 50%), -57px 159px hsl(858.6, 100%, 50%), -57px 160px hsl(864, 100%, 50%), -56px 161px hsl(869.4, 100%, 50%), -55px 162px hsl(874.8, 100%, 50%), -55px 163px hsl(880.2, 100%, 50%), -54px 164px hsl(885.6, 100%, 50%), -53px 165px hsl(891, 100%, 50%), -52px 166px hsl(896.4, 100%, 50%), -51px 167px hsl(901.8, 100%, 50%), -50px 168px hsl(907.2, 100%, 50%), -49px 169px hsl(912.6, 100%, 50%), -48px 170px hsl(918, 100%, 50%), -47px 171px hsl(923.4, 100%, 50%), -46px 172px hsl(928.8, 100%, 50%), -45px 173px hsl(934.2, 100%, 50%), -43px 174px hsl(939.6, 100%, 50%), -42px 175px hsl(945, 100%, 50%), -41px 176px hsl(950.4, 100%, 50%), -39px 177px hsl(955.8, 100%, 50%), -38px 178px hsl(961.2, 100%, 50%), -36px 179px hsl(966.6, 100%, 50%), -35px 180px hsl(972, 100%, 50%), -33px 181px hsl(977.4, 100%, 50%), -32px 182px hsl(982.8, 100%, 50%), -30px 183px hsl(988.2, 100%, 50%), -28px 184px hsl(993.6, 100%, 50%), -27px 185px hsl(999, 100%, 50%), -25px 186px hsl(1004.4, 100%, 50%), -23px 187px hsl(1009.8, 100%, 50%), -22px 188px hsl(1015.2, 100%, 50%), -20px 189px hsl(1020.6, 100%, 50%), -18px 190px hsl(1026, 100%, 50%), -16px 191px hsl(1031.4, 100%, 50%), -14px 192px hsl(1036.8, 100%, 50%), -13px 193px hsl(1042.2, 100%, 50%), -11px 194px hsl(1047.6, 100%, 50%), -9px 195px hsl(1053, 100%, 50%), -7px 196px hsl(1058.4, 100%, 50%), -5px 197px hsl(1063.8, 100%, 50%), -3px 198px hsl(1069.2, 100%, 50%), -1px 199px hsl(1074.6, 100%, 50%), -1px 200px hsl(1080, 100%, 50%), 1px 201px hsl(1085.4, 100%, 50%), 3px 202px hsl(1090.8, 100%, 50%), 5px 203px hsl(1096.2, 100%, 50%), 7px 204px hsl(1101.6, 100%, 50%), 9px 205px hsl(1107, 100%, 50%), 11px 206px hsl(1112.4, 100%, 50%), 13px 207px hsl(1117.8, 100%, 50%), 14px 208px hsl(1123.2, 100%, 50%), 16px 209px hsl(1128.6, 100%, 50%), 18px 210px hsl(1134, 100%, 50%), 20px 211px hsl(1139.4, 100%, 50%), 22px 212px hsl(1144.8, 100%, 50%), 23px 213px hsl(1150.2, 100%, 50%), 25px 214px hsl(1155.6, 100%, 50%), 27px 215px hsl(1161, 100%, 50%), 28px 216px hsl(1166.4, 100%, 50%), 30px 217px hsl(1171.8, 100%, 50%), 32px 218px hsl(1177.2, 100%, 50%), 33px 219px hsl(1182.6, 100%, 50%), 35px 220px hsl(1188, 100%, 50%), 36px 221px hsl(1193.4, 100%, 50%), 38px 222px hsl(1198.8, 100%, 50%), 39px 223px hsl(1204.2, 100%, 50%), 41px 224px hsl(1209.6, 100%, 50%), 42px 225px hsl(1215, 100%, 50%), 43px 226px hsl(1220.4, 100%, 50%), 45px 227px hsl(1225.8, 100%, 50%), 46px 228px hsl(1231.2, 100%, 50%), 47px 229px hsl(1236.6, 100%, 50%), 48px 230px hsl(1242, 100%, 50%), 49px 231px hsl(1247.4, 100%, 50%), 50px 232px hsl(1252.8, 100%, 50%), 51px 233px hsl(1258.2, 100%, 50%), 52px 234px hsl(1263.6, 100%, 50%), 53px 235px hsl(1269, 100%, 50%), 54px 236px hsl(1274.4, 100%, 50%), 55px 237px hsl(1279.8, 100%, 50%), 55px 238px hsl(1285.2, 100%, 50%), 56px 239px hsl(1290.6, 100%, 50%), 57px 240px hsl(1296, 100%, 50%), 57px 241px hsl(1301.4, 100%, 50%), 58px 242px hsl(1306.8, 100%, 50%), 58px 243px hsl(1312.2, 100%, 50%), 58px 244px hsl(1317.6, 100%, 50%), 59px 245px hsl(1323, 100%, 50%), 59px 246px hsl(1328.4, 100%, 50%), 59px 247px hsl(1333.8, 100%, 50%), 59px 248px hsl(1339.2, 100%, 50%), 59px 249px hsl(1344.6, 100%, 50%), 60px 250px hsl(1350, 100%, 50%), 59px 251px hsl(1355.4, 100%, 50%), 59px 252px hsl(1360.8, 100%, 50%), 59px 253px hsl(1366.2, 100%, 50%), 59px 254px hsl(1371.6, 100%, 50%), 59px 255px hsl(1377, 100%, 50%), 58px 256px hsl(1382.4, 100%, 50%), 58px 257px hsl(1387.8, 100%, 50%), 58px 258px hsl(1393.2, 100%, 50%), 57px 259px hsl(1398.6, 100%, 50%), 57px 260px hsl(1404, 100%, 50%), 56px 261px hsl(1409.4, 100%, 50%), 55px 262px hsl(1414.8, 100%, 50%), 55px 263px hsl(1420.2, 100%, 50%), 54px 264px hsl(1425.6, 100%, 50%), 53px 265px hsl(1431, 100%, 50%), 52px 266px hsl(1436.4, 100%, 50%), 51px 267px hsl(1441.8, 100%, 50%), 50px 268px hsl(1447.2, 100%, 50%), 49px 269px hsl(1452.6, 100%, 50%), 48px 270px hsl(1458, 100%, 50%), 47px 271px hsl(1463.4, 100%, 50%), 46px 272px hsl(1468.8, 100%, 50%), 45px 273px hsl(1474.2, 100%, 50%), 43px 274px hsl(1479.6, 100%, 50%), 42px 275px hsl(1485, 100%, 50%), 41px 276px hsl(1490.4, 100%, 50%), 39px 277px hsl(1495.8, 100%, 50%), 38px 278px hsl(1501.2, 100%, 50%), 36px 279px hsl(1506.6, 100%, 50%), 35px 280px hsl(1512, 100%, 50%), 33px 281px hsl(1517.4, 100%, 50%), 32px 282px hsl(1522.8, 100%, 50%), 30px 283px hsl(1528.2, 100%, 50%), 28px 284px hsl(1533.6, 100%, 50%), 27px 285px hsl(1539, 100%, 50%), 25px 286px hsl(1544.4, 100%, 50%), 23px 287px hsl(1549.8, 100%, 50%), 22px 288px hsl(1555.2, 100%, 50%), 20px 289px hsl(1560.6, 100%, 50%), 18px 290px hsl(1566, 100%, 50%), 16px 291px hsl(1571.4, 100%, 50%), 14px 292px hsl(1576.8, 100%, 50%), 13px 293px hsl(1582.2, 100%, 50%), 11px 294px hsl(1587.6, 100%, 50%), 9px 295px hsl(1593, 100%, 50%), 7px 296px hsl(1598.4, 100%, 50%), 5px 297px hsl(1603.8, 100%, 50%), 3px 298px hsl(1609.2, 100%, 50%), 1px 299px hsl(1614.6, 100%, 50%), 2px 300px hsl(1620, 100%, 50%), -1px 301px hsl(1625.4, 100%, 50%), -3px 302px hsl(1630.8, 100%, 50%), -5px 303px hsl(1636.2, 100%, 50%), -7px 304px hsl(1641.6, 100%, 50%), -9px 305px hsl(1647, 100%, 50%), -11px 306px hsl(1652.4, 100%, 50%), -13px 307px hsl(1657.8, 100%, 50%), -14px 308px hsl(1663.2, 100%, 50%), -16px 309px hsl(1668.6, 100%, 50%), -18px 310px hsl(1674, 100%, 50%), -20px 311px hsl(1679.4, 100%, 50%), -22px 312px hsl(1684.8, 100%, 50%), -23px 313px hsl(1690.2, 100%, 50%), -25px 314px hsl(1695.6, 100%, 50%), -27px 315px hsl(1701, 100%, 50%), -28px 316px hsl(1706.4, 100%, 50%), -30px 317px hsl(1711.8, 100%, 50%), -32px 318px hsl(1717.2, 100%, 50%), -33px 319px hsl(1722.6, 100%, 50%), -35px 320px hsl(1728, 100%, 50%), -36px 321px hsl(1733.4, 100%, 50%), -38px 322px hsl(1738.8, 100%, 50%), -39px 323px hsl(1744.2, 100%, 50%), -41px 324px hsl(1749.6, 100%, 50%), -42px 325px hsl(1755, 100%, 50%), -43px 326px hsl(1760.4, 100%, 50%), -45px 327px hsl(1765.8, 100%, 50%), -46px 328px hsl(1771.2, 100%, 50%), -47px 329px hsl(1776.6, 100%, 50%), -48px 330px hsl(1782, 100%, 50%), -49px 331px hsl(1787.4, 100%, 50%), -50px 332px hsl(1792.8, 100%, 50%), -51px 333px hsl(1798.2, 100%, 50%), -52px 334px hsl(1803.6, 100%, 50%), -53px 335px hsl(1809, 100%, 50%), -54px 336px hsl(1814.4, 100%, 50%), -55px 337px hsl(1819.8, 100%, 50%), -55px 338px hsl(1825.2, 100%, 50%), -56px 339px hsl(1830.6, 100%, 50%), -57px 340px hsl(1836, 100%, 50%), -57px 341px hsl(1841.4, 100%, 50%), -58px 342px hsl(1846.8, 100%, 50%), -58px 343px hsl(1852.2, 100%, 50%), -58px 344px hsl(1857.6, 100%, 50%), -59px 345px hsl(1863, 100%, 50%), -59px 346px hsl(1868.4, 100%, 50%), -59px 347px hsl(1873.8, 100%, 50%), -59px 348px hsl(1879.2, 100%, 50%), -59px 349px hsl(1884.6, 100%, 50%), -60px 350px hsl(1890, 100%, 50%), -59px 351px hsl(1895.4, 100%, 50%), -59px 352px hsl(1900.8, 100%, 50%), -59px 353px hsl(1906.2, 100%, 50%), -59px 354px hsl(1911.6, 100%, 50%), -59px 355px hsl(1917, 100%, 50%), -58px 356px hsl(1922.4, 100%, 50%), -58px 357px hsl(1927.8, 100%, 50%), -58px 358px hsl(1933.2, 100%, 50%), -57px 359px hsl(1938.6, 100%, 50%), -57px 360px hsl(1944, 100%, 50%), -56px 361px hsl(1949.4, 100%, 50%), -55px 362px hsl(1954.8, 100%, 50%), -55px 363px hsl(1960.2, 100%, 50%), -54px 364px hsl(1965.6, 100%, 50%), -53px 365px hsl(1971, 100%, 50%), -52px 366px hsl(1976.4, 100%, 50%), -51px 367px hsl(1981.8, 100%, 50%), -50px 368px hsl(1987.2, 100%, 50%), -49px 369px hsl(1992.6, 100%, 50%), -48px 370px hsl(1998, 100%, 50%), -47px 371px hsl(2003.4, 100%, 50%), -46px 372px hsl(2008.8, 100%, 50%), -45px 373px hsl(2014.2, 100%, 50%), -43px 374px hsl(2019.6, 100%, 50%), -42px 375px hsl(2025, 100%, 50%), -41px 376px hsl(2030.4, 100%, 50%), -39px 377px hsl(2035.8, 100%, 50%), -38px 378px hsl(2041.2, 100%, 50%), -36px 379px hsl(2046.6, 100%, 50%), -35px 380px hsl(2052, 100%, 50%), -33px 381px hsl(2057.4, 100%, 50%), -32px 382px hsl(2062.8, 100%, 50%), -30px 383px hsl(2068.2, 100%, 50%), -28px 384px hsl(2073.6, 100%, 50%), -27px 385px hsl(2079, 100%, 50%), -25px 386px hsl(2084.4, 100%, 50%), -23px 387px hsl(2089.8, 100%, 50%), -22px 388px hsl(2095.2, 100%, 50%), -20px 389px hsl(2100.6, 100%, 50%), -18px 390px hsl(2106, 100%, 50%), -16px 391px hsl(2111.4, 100%, 50%), -14px 392px hsl(2116.8, 100%, 50%), -13px 393px hsl(2122.2, 100%, 50%), -11px 394px hsl(2127.6, 100%, 50%), -9px 395px hsl(2133, 100%, 50%), -7px 396px hsl(2138.4, 100%, 50%), -5px 397px hsl(2143.8, 100%, 50%), -3px 398px hsl(2149.2, 100%, 50%), -1px 399px hsl(2154.6, 100%, 50%);')

/*
|--------------------------------------------------------------------------
| INIT STUFF
|--------------------------------------------------------------------------
*/
var header = document.querySelector('big-header');
var dialog = document.querySelector('paper-dialog');
var posterrortoast = document.querySelector('#posterrortoast');
var tabs = document.querySelector('paper-dialog paper-tabs');
var postslist = document.querySelector('posts-list');
var middle = document.querySelector('paper-dialog .middle');
var dialogcancel = document.querySelector('paper-dialog .cancel');
var dialogshare = document.querySelector('paper-dialog .share');
var progress = document.querySelector('paper-dialog paper-progress');
var dialogxhr = document.querySelector('#dialogxhr');

var inputAll = document.querySelectorAll('paper-dialog .middle paper-input');

//show dialog
header.addEventListener('addtap', function(){
    dialog.toggle();

    //fix for polymer bug
    setTimeout(function(){
        for (var i = 0; i < inputAll.length; ++i) {
            inputAll[i].labelChanged();
        }
    }, 200);
});

tabs.addEventListener('core-select', function(){
    removeClass(middle, 'on0');
    removeClass(middle, 'on1');
    addClass(middle, 'on'+tabs.selected);
    inputAll[0].fire('keyup');
})

// inputAll[0].addEventListener('keydown', function(e){
//     if(e.keyCode == 13){
//         inputAll[1].focus();
//     }
// });

// inputAll[1].addEventListener('keydown', function(e){
//     if(e.keyCode == 13){
//         dialogshare.click();
//     }
// });

// inputAll[2].addEventListener('keydown', function(e){
//     if(e.keyCode == 13){
//         inputAll[3].focus();
//     }
// });

//cancel
dialogcancel.addEventListener('tap', function(){
    dialog.toggle();
    setTimeout(function(){
        dialog.clearInput();
    }, 150);
});

dialog.clearInput = function(){
    for (var i = 0; i < inputAll.length; ++i) {
        inputAll[i].value = '';
    }
}

dialogshare.addEventListener('tap', function(){
    var title = link = text = "";
    if(tabs.selected == 0){
        var title = inputAll[0].inputValue;
        var link = linkFilter(inputAll[1].inputValue);
    }else{
        var title = inputAll[2].inputValue;
        var text = inputAll[3].inputValue;
    }

    dialogshare.setEnableValue(false);
    progress.startProgress();
    dialogxhr.request({
        url: '/api/post/create/',
        method: 'POST',
        body: objectToFormdata({
            title: title,
            link: link,
            text: text
        }),
        responseType: 'json',
        callback: function(data, extra){
            if(extra.status == 200){
                insertNewPost(data.id, title, link);
                progress.stopProgress();
                dialog.toggle();
                dialog.clearInput();
            }else{
                progress.stopProgress();
                posterrortoast.show();
            }
            dialogshare.setEnableValue(true);
        }
    });
});

dialogcancel.addEventListener('keypress', function(e){
    if(e.keyCode == 13){
        dialogcancel.fire('tap');
    }
});

dialogshare.addEventListener('keypress', function(e){
    if(e.keyCode == 13){
        dialogshare.fire('tap');
    }
});

function insertNewPost(id, title, link){
    if(postslist && (postslist.listtype == 'hottest' || postslist.listtype == 'latest' ||
        (postslist.userpage && postslist.userpage == window.inuser))){
        postslist.createNewPost(id, title, link);
    }
}

for (var i = 0; i < inputAll.length; ++i) {
    inputAll[i].addEventListener('keyup', function(){
        if(tabs.selected == 0){
            var valid = inputAll[0].inputValue && inputAll[1].inputValue && !hasClass(inputAll[1], 'invalid');
        }else{
            var valid = inputAll[2].inputValue && inputAll[3].inputValue;
        }
        dialogshare.setEnableValue(valid);
    });
}

progress.startProgress = function(){
    if(this.stopnow){
        this.stopnow = false;
        return;
    }

    if (this.value < 100) {
        this.value += 1;
    } else {
        this.value = 0;
    }
    this.async(this.startProgress);
    return;

    setTimeout(this.startProgress, 17);
    try{
        this.asyncFire();
    }catch(e){
        // I don't know why polymer is throwing an exception,
        // I wish the docs were more fleshed out - or I could
        // just talk to someone who actually made polymer...
        // because this is clearly a bug
    }
}

progress.stopProgress = function(){
    this.value = 0;
    this.stopnow = true;
}

dialogshare.setEnableValue = function(value){
    if(value){
        dialogshare.removeAttribute('disabled');
    }else{
        dialogshare.setAttribute('disabled', true);
    }
}


/*
|--------------------------------------------------------------------------
| QUOTE STUFF
|--------------------------------------------------------------------------
*/
var quotes = "The only way of finding the limits of the possible is by going beyond them into the impossible.|Arthur C. Clarke"+
             "~You are already naked. There is no reason not to follow your heart.|Steve Jobs"+
             "~When people think you're dying they really, really listen to you instead of just waiting for their turn to speak.|Fight Club"+
             "~Oh, dinner at eight, Harold. And do try and be a little more vivacious.|Harold and Maude"+
             "~I think people place too much emphasis on their careers.  I wish we could all live in the mountains at high altitude. That's where I see myself in five years.|Groundhog Day"+
             "~There are no mistakes, only opportunities.|Tina Fey"+
             "~I have over 2 million followers now on Google Plus.|Larry Page"+
             "~Very little is needed to make a happy life; it is all within yourself, in your way of thinking.|Marcus Aurelius Antoninus"+
             "~If something is important enough, even if the odds are against you, you should still do it.|Elon Musk (my hero)"+
             "~Screw it, let's do it.|Richard Branson"+
             "~The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart.|Helen Keller"+
             "~Do not wait for leaders, do it alone, person to person.|Mother Teresa"+
             "~If you obey all the rules, you miss all the fun.|Audrey Hepburn"+
             "~After obsessively Googling symptoms for four hours, I discovered 'obsessively Googling symptoms' is a symptom of hypochondria.|Stephen Colbert"+
             "~You can be the crazy kid in some lady's garage going on and on and on about how you're going to change the world and then you can go out and actually do it.|Susan Wojcicki";
function randomQuote(){
    var built = quotes.split('~');

    var item = built[Math.floor(Math.random()*built.length)];

    return item.split('|');
}
