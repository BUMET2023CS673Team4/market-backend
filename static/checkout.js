initialize();

function getCookie(cookieName) {
  const cookies = document.cookie.split('; ');

  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].split('=');
    if (cookie[0] === cookieName) {
      return cookie[1];
    }
  }

  return null;
}

// Create a Checkout Session as soon as the page loads
async function initialize() {
  const stripe_key = await fetch("/api/stripe-public-key/", {
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  });
  const { public_key } = await stripe_key.json();
  const stripe = Stripe(public_key);
  const response = await fetch("/api/create-checkout-session/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  });

  const { client_secret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret: client_secret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}