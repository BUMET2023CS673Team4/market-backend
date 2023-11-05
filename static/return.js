initialize();

async function initialize() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const sessionId = urlParams.get('stripe_sid');
  const response = await fetch(`/api/session-status?stripe_sid=${sessionId}`, {
    method: 'GET',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  
  });
  const session = await response.json();

  if (session.status == 'open') {
    window.replace('/checkout.html')
  } else if (session.status == 'complete') {
    document.getElementById('success').classList.remove('hidden');
    document.getElementById('customer-email').textContent = session.customer_email
  }
}