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
        return 'just moments ago';
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
            .replace(/>/g, '&gt;');
}
function stuffEncode(text){
    var result = linkify(text);
    result = result.replace(/(?:\r\n|\r|\n)/g, '<br />');
    result = htmlEscape(text);
    return result;
}
function prepend(child, parent){
    parent.insertBefore(child,parent.firstChild);
}

console.log('%cGoogle', 'background: green; color: white; display: block;');

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
header.addEventListener('tap', function(){
    dialog.toggle();

    setTimeout(function(){
        for (var i = 0; i < inputAll.length; ++i) {
            inputAll[i].labelChanged();
        }
    }, 100);
});

tabs.addEventListener('core-select', function(){
    removeClass(middle, 'on0');
    removeClass(middle, 'on1');
    addClass(middle, 'on'+tabs.selected);
    inputAll[0].fire('keyup');
})

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
        var link = inputAll[1].inputValue;
    }else{
        var title = inputAll[2].inputValue;
        var text = inputAll[3].inputValue;
    }

    dialogshare.setEnableValue(false);
    progress.startProgress();
    dialogxhr.request({
        url: '/api/post/create',
        method: 'POST',
        params: {
            title: title,
            link: '',
            text: ''
        },
        reponseType: 'json',
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
