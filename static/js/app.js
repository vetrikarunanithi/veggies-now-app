// JavaScript helper to show styled alerts instead of default alert()
function showAlert(message, type = 'success') {
  let alertDiv = document.createElement('div');
  alertDiv.className = `custom-alert ${type} show`;
  alertDiv.textContent = message;
  document.body.appendChild(alertDiv);

  setTimeout(() => {
    alertDiv.classList.remove('show');
    setTimeout(() => document.body.removeChild(alertDiv), 300);
  }, 3000);
}

function postData(url = '', data = {}) {
  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then((r) => r.json());
}

function addToCart(productId) {
  postData('/add-to-cart', { product_id: productId, qty: 1 }).then((res) => {
    showAlert(res.message || 'Added to cart', res.ok ? 'success' : 'error');
  });
}

function updateQty(productId, qty) {
  postData('/cart/update', { product_id: productId, qty: qty }).then((res) => {
    if (res.ok) location.reload();
    else showAlert(res.message || 'Failed to update quantity', 'error');
  });
}

function removeFromCart(productId) {
  postData('/cart/remove', { product_id: productId }).then((res) => {
    if (res.ok) location.reload();
    else showAlert(res.message || 'Failed to remove item', 'error');
  });
}
