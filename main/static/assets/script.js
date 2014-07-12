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
var removeClass = function (elem, className) {
    var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ') + ' ';
    if (hasClass(elem, className)) {
        while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
            newClass = newClass.replace(' ' + className + ' ', ' ');
        }
        elem.className = newClass.replace(/^\s+|\s+$/g, '');
    }
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

/*
|--------------------------------------------------------------------------
| INIT STUFF
|--------------------------------------------------------------------------
*/
var header = document.querySelector('big-header');
var dialog = document.querySelector('paper-dialog');
var tabs = document.querySelector('paper-dialog paper-tabs');
var postslist = document.querySelector('posts-list');
var middle = document.querySelector('paper-dialog .middle');
var dialogcancel = document.querySelector('paper-dialog .cancel');
var dialogshare = document.querySelector('paper-dialog .share');
var progress = document.querySelector('paper-dialog paper-progress');

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
})

//cancel
dialogcancel.addEventListener('tap', function(){
    dialog.toggle();
    setTimeout(function(){
        for (var i = 0; i < inputAll.length; ++i) {
            inputAll[i].value = '';
        }
    }, 150);
});

dialogshare.addEventListener('tap', function(){
    if(tabs.selected == 0){
        var type = 0;
        var page = document.querySelector('paper-dialog .middle .page0');
    }else{
        var type = 1;
        var page = document.querySelector('paper-dialog .middle .page1');
    }

    var title = Sizzle('.title', page)[0].inputValue;
    var field = Sizzle('.field', page)[0].inputValue;

    //insert
    if(postslist && (postslist.listtype == 'hottest' || postslist.listtype == 'latest')){

    }
    var newPost = document.createElement('indiv-post');
    newPost.setAttribute('score', 1);
    newPost.setAttribute('postid', 19);
    newPost.setAttribute('mark', 1);
    newPost.setAttribute('timestamp', 1404831074000);
    newPost.setAttribute('author', 'shoes');
    document.querySelector('posts-list').insertBefore(newPost, document.querySelector('posts-list').firstChild);
    var height = newPost.offsetHeight;
    // newPost.style.height = '0px';
    var player = document.timeline.play(new Animation(newPost, [
          {height: '0px', transform: "rotateX(90deg)"}, 
          {height: height+'px', transform: "rotateX(0deg)"}
        ],
        {
          direction: "alternate",
          duration: 500,
          iterations: 1,
          easing: 'cubic-bezier(.4,0,.2,1)'
        }));

    progress.startProgress();
});

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
        this.value = 0;
        return;
    }

    if (this.value < 100) {
        this.value += 1;
    } else {
        this.value = 0
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
    }
}

dialogshare.setEnableValue = function(value){
    if(value){
        dialogshare.removeAttribute('disabled');
    }else{
        dialogshare.setAttribute('disabled', true);
    }
}

progress.stopProgress = function(){
    this.stopnow = true;
}

function submitPost(title, field, type){

}