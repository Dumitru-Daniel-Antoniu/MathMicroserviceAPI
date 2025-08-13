const channel = new BroadcastChannel('authentication');
channel.onmessage = (event) => {
  if(event.data === 'login' || event.data === 'logout') {
    if(window.location.pathname === '/statistics') {
      window.location.href = '/statistics';
    }
    else window.location.reload();
  }
}