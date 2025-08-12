const channel = new BroadcastChannel('authentication');
channel.onmessage = (event) => {
  if (event.data === 'login') {
    window.location.reload();
  }
}