// Forms: errors are checked on submit and listed in a summary at the top that links to each field,
// with the message repeated beside the field. This static build is not connected to the Authority's
// systems, so forms marked data-form-preview show a notice instead of sending. In WordPress the same
// markup posts to admin-post.php: drop data-form-preview and add the nonce fields there.
const MAX_MB = 10;

export default function (forms) { forms.forEach(init); }

function init(form) {
  form.noValidate = true;
  form.addEventListener('submit', (e) => {
    form.querySelector('.ca-form-notice')?.remove();
    const errors = [...form.querySelectorAll('.ca-field, .ca-group')].map(check).filter(Boolean);
    summary(form, errors);
    if (errors.length) { e.preventDefault(); return; }
    if (form.hasAttribute('data-form-preview')) { e.preventDefault(); notice(form); }
  });
  // once a field has been flagged, clear the message as soon as it is fixed
  const recheck = (e) => { const f = e.target.closest('.ca-field, .ca-group'); if (f?.classList.contains('is-invalid')) check(f); };
  form.addEventListener('input', recheck);
  form.addEventListener('change', recheck);
}

// returns { id, message } when the field (or group of choices) is invalid, after marking it up
function check(field) {
  const controls = [...field.querySelectorAll('input, select, textarea')];
  const first = controls[0];
  if (!first) return null;
  let message = '';
  if (field.matches('.ca-group')) {
    const required = field.hasAttribute('data-required');
    if (required && !controls.some((c) => c.checked)) message = field.dataset.error || 'Select an option';
  } else if (first.type === 'checkbox') {
    if (first.required && !first.checked) message = field.dataset.error || 'Tick the box to continue';
  } else if (first.type === 'file') {
    const file = first.files?.[0];
    if (file && file.size > MAX_MB * 1048576) message = `The file must be smaller than ${MAX_MB} MB`;
  } else {
    const value = first.value.trim();
    if (first.required && !value) message = field.dataset.error || 'Fill in this field';
    else if (value && first.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) message = 'Enter an email address in the right format, like name@example.com';
    else if (value && first.type === 'tel' && !/^[+\d][\d\s()-]{6,}$/.test(value)) message = 'Enter a phone number using digits, like 0712 345678';
  }
  mark(field, controls, message);
  return message ? { id: first.id, message } : null;
}

function mark(field, controls, message) {
  const id = `${controls[0].id}-error`;
  field.classList.toggle('is-invalid', !!message);
  field.querySelector('.ca-error')?.remove();
  controls.forEach((c) => {
    const ids = (c.getAttribute('aria-describedby') || '').split(' ').filter((x) => x && x !== id);
    if (message) { ids.unshift(id); c.setAttribute('aria-invalid', 'true'); } else c.removeAttribute('aria-invalid');
    if (ids.length) c.setAttribute('aria-describedby', ids.join(' ')); else c.removeAttribute('aria-describedby');
  });
  if (!message) return;
  const p = document.createElement('p');
  p.className = 'ca-error';
  p.id = id;
  p.textContent = message;
  const label = field.querySelector(':scope > label, :scope > legend');
  (label?.nextElementSibling?.matches('.ca-hint') ? label.nextElementSibling : label)?.after(p);
}

function summary(form, errors) {
  form.querySelector('.ca-error-summary')?.remove();
  if (!errors.length) return;
  const box = document.createElement('div');
  box.className = 'ca-error-summary';
  box.tabIndex = -1;
  box.setAttribute('role', 'alert');
  box.innerHTML = `<h2>There ${errors.length === 1 ? 'is a problem' : `are ${errors.length} problems`} with your answers</h2><ul></ul>`;
  errors.forEach(({ id, message }) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = `#${id}`;
    a.textContent = message;
    a.addEventListener('click', (e) => { e.preventDefault(); document.getElementById(id)?.focus(); });
    li.append(a);
    box.querySelector('ul').append(li);
  });
  form.prepend(box);
  box.focus();
}

function notice(form) {
  const sprite = document.querySelector('use')?.getAttribute('href').split('#')[0] || '/assets/icons/sprite.svg';
  const box = document.createElement('div');
  box.className = 'ca-form-notice';
  box.tabIndex = -1;
  box.setAttribute('role', 'status');
  box.innerHTML = `<svg class="ca-icon" aria-hidden="true"><use href="${sprite}#info"/></svg>
    <p class="ca-form-notice__title">Your answers are complete</p>
    <p>Nothing has been sent: this preview of the new website is not yet connected to the Authority’s systems.</p>`;
  form.prepend(box);
  box.focus();
}
