if(!window.dash_clientside) {window.dash_clientside = {};}

window.dash_clientside.clientside = {

  stickyHeader: function(id) {
    let header = document.getElementById('header');
    let sticky = header.offsetTop;

    window.onscroll = function() {
      
      // Only enabled for large screen sizes
      if (window.innerWidth >= 1024 && window.pageYOffset > sticky) {
        header.classList.add('sticky');
      } else {
        header.classList.remove('sticky');
      }
    };

    return window.dash_clientside.no_update
  },
}