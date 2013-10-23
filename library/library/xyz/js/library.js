$(function(){
  //set up breadcrumbs
  host='http://localhost:8009/';
  base='http://schoolserver/bibliotheque/list/';
  pageno=$('#gallery').attr('pageno');
  collection=$('#gallery').attr('collection_id');
  title=$('#gallery').attr('title');
  lastpage=$('#gallery').attr('lastpage');
  if(typeof(title)=='undefined'){
    title='Library'
  };
  next=parseInt(pageno)+1;
  back=pageno-1;
  /* set title in head */
  $('head title')
      .empty()
      .text(title);
  /* set navbar: linkHome, title,  linkQuit */
  $('<div>',{
      id:'linkHome',
      title:'Home',
      click:function(){
         window.location = host+'content/index.html';
      }
      })
      .appendTo('#breadcrumb');
  if(title != 'Library'){
      $('<div>',{
        id: 'linkMain',
        title: 'Main',
        click:function(){
          window.location = 'http://schoolserver/bibliotheque/'
        }
      })
      .appendTo('#breadcrumb');
  };
  $('<div>',{
      id:'title'
      })
  $('#title')
      .html('<span>'+title+'</span>');
  $('<img>',{
      src:'http://localhost:8009/content/karma/image/title_block_lt.png',
      id:'title_img_l'
      })
      .prependTo('#title');
  $('<img>',{
      src:'http://localhost:8009/content/karma/image/title_block_rt.png',
      id:'title_img_r'
      })
      .appendTo('#title');
  $('<div>',{
      id:'linkQuit',
      title:'Quit',
      click:function(){
        window.close();
      } 
      })
  // now do the '#footer'
  if(pageno>0){
    $('<div>',{
         id:'linkPrevScreen',
         title:'Previous',
         click:function(){
           window.location=base+collection+'/'+back;
         }
    })
    .appendTo('#footer');
  };
  if(next<lastpage){
    $('<div>',{
         id: 'linkNextScreen',
         title:'Next',
         click:function(){
           window.location=base+collection+'/'+next;
         }
    })
    .appendTo('#footer');
  }
});
