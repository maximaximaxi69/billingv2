const invoiceForm = document.getElementById('invoice-form');
const noteForm = document.getElementById('note-form');
const clientForm = document.getElementById('client-form');
const issuerForm = document.getElementById('issuer-form');

const invoiceList = document.getElementById('invoice-list');
const noteList = document.getElementById('note-list');
const typeSelect = document.getElementById('invoice_type');
const advanceFields = document.getElementById('advance-fields');
const filterType = document.getElementById('filter-type');
const sortBy = document.getElementById('sort-by');
const searchQ = document.getElementById('search-q');
const issuerPartySelect = document.getElementById('issuer_party_id');
const clientPartySelect = document.getElementById('client_party_id');
const openInvoiceFormBtn = document.getElementById('open-invoice-form');
const invoiceFormCard = document.getElementById('invoice-form-card');
const themeToggle = document.getElementById('theme-toggle');

let clients = [];
let issuers = [];

function renderIcons() {
  if (window.lucide) window.lucide.createIcons();
}

function toggleTheme() {
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
}

function hydrateTheme() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') document.documentElement.classList.add('dark');
}

function updateAdvanceFields() {
  advanceFields.classList.toggle('hidden', typeSelect.value !== 'advance_final');
}

function fmtParty(p) {
  return [
    p.name,
    p.reg_no ? `Reģ. Nr.: ${p.reg_no}` : null,
    p.vat_no ? `PVN: ${p.vat_no}` : null,
    p.legal_address ? `Adrese: ${p.legal_address}` : null,
    p.bank_name ? `Banka: ${p.bank_name}` : null,
    p.bank_account ? `Konts: ${p.bank_account}` : null,
    p.email ? `E-pasts: ${p.email}` : null,
    p.phone ? `Tālr.: ${p.phone}` : null,
  ].filter(Boolean).join('\n');
}

function fillPartySelect(selectEl, rows, placeholder) {
  selectEl.innerHTML = `<option value="">${placeholder}</option>` + rows.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
}

async function loadParties() {
  clients = await fetch('/api/parties?party_type=client').then(r => r.json());
  issuers = await fetch('/api/parties?party_type=issuer').then(r => r.json());
  fillPartySelect(clientPartySelect, clients, 'Izvēlies klientu');
  fillPartySelect(issuerPartySelect, issuers, 'Izvēlies piestādītāja profilu');
}

issuerPartySelect.addEventListener('change', () => {
  const party = issuers.find(x => String(x.id) === issuerPartySelect.value);
  if (!party) return;
  invoiceForm.seller_name.value = party.name;
  invoiceForm.seller_details.value = fmtParty(party);
});

clientPartySelect.addEventListener('change', () => {
  const party = clients.find(x => String(x.id) === clientPartySelect.value);
  if (!party) return;
  invoiceForm.client_name.value = party.name;
  invoiceForm.client_details.value = fmtParty(party);
});

typeSelect.addEventListener('change', updateAdvanceFields);
themeToggle.addEventListener('click', toggleTheme);

clientForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(clientForm);
  const payload = Object.fromEntries(f.entries());
  payload.party_type = 'client';
  const res = await fetch('/api/parties', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!res.ok) return alert('Neizdevās saglabāt klientu');
  clientForm.reset();
  await loadParties();
});

issuerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(issuerForm);
  const payload = Object.fromEntries(f.entries());
  payload.party_type = 'issuer';
  const res = await fetch('/api/parties', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!res.ok) return alert('Neizdevās saglabāt profilu');
  issuerForm.reset();
  await loadParties();
});

invoiceForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(invoiceForm);
  const payload = {
    number: f.get('number'),
    invoice_type: f.get('invoice_type'),
    issue_date: f.get('issue_date'),
    due_date: f.get('due_date'),
    seller_name: f.get('seller_name'),
    seller_details: f.get('seller_details') || null,
    client_name: f.get('client_name'),
    client_details: f.get('client_details') || null,
    seller_party_id: f.get('issuer_party_id') ? Number(f.get('issuer_party_id')) : null,
    client_party_id: f.get('client_party_id') ? Number(f.get('client_party_id')) : null,
    notes: f.get('notes') || null,
    previous_paid_amount: f.get('previous_paid_amount') ? Number(f.get('previous_paid_amount')) : null,
    previous_advance_reference: f.get('previous_advance_reference') || null,
    items: [{
      description: f.get('item_description'),
      quantity: Number(f.get('item_quantity')),
      unit: f.get('item_unit'),
      unit_price: Number(f.get('item_price')),
    }],
  };

  const res = await fetch('/api/invoices', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  if (!res.ok) return alert('Kļūda, saglabājot rēķinu');
  invoiceForm.reset();
  updateAdvanceFields();
  invoiceFormCard.classList.add('hidden');
  if (!res.ok) {
    alert('Kļūda, saglabājot rēķinu');
    return;
  }
  invoiceForm.reset();
  updateAdvanceFields();
  await loadInvoices();
});

noteForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(noteForm);
  const payload = {
    number: f.get('number'),
    issue_date: f.get('issue_date'),
    issuer_name: f.get('issuer_name'),
    receiver_name: f.get('receiver_name'),
    delivery_address: f.get('delivery_address'),
    items: [{
      description: f.get('item_description'),
      quantity: Number(f.get('item_quantity')),
      unit: f.get('item_unit'),
    }],
  };

  const res = await fetch('/api/delivery-notes', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  if (!res.ok) return alert('Kļūda, saglabājot pavadzīmi');
  if (!res.ok) {
    alert('Kļūda, saglabājot pavadzīmi');
    return;
  }
  noteForm.reset();
  await loadNotes();
});

async function loadInvoices() {
  const p = new URLSearchParams();
  if (filterType.value) p.set('invoice_type', filterType.value);
  if (searchQ.value.trim()) p.set('q', searchQ.value.trim());
  if (sortBy.value) p.set('sort', sortBy.value);

  const data = await fetch(`/api/invoices?${p.toString()}`).then(r => r.json());
  if (!data.length) {
    invoiceList.innerHTML = `<div class="p-6 text-center text-slate-400">Nav rēķinu. Nospiediet “+ Jauns rēķins”, lai izveidotu.</div>`;
    return;
  }

  invoiceList.innerHTML = data.map(i => `
    <div class="grid grid-cols-7 items-center p-3 border-t border-slate-700 text-sm">
      <div>${i.number}</div>
      <div>${i.client_name}</div>
      <div>${i.issue_date}</div>
      <div>${i.due_date}</div>
      <div>${i.total.toFixed(2)} EUR</div>
      <div>${i.payable.toFixed(2)} EUR</div>
      <div><a class="text-indigo-300 underline" href="/api/invoices/${i.id}/pdf">PDF</a></div>
    </div>
  `).join('');
  invoiceList.innerHTML = data.map(i => `
    <div class="border dark:border-slate-700 rounded-lg p-3 flex items-center justify-between bg-slate-50 dark:bg-slate-800/40">
      <div>
        <p class="font-semibold">${i.number} · <span class="uppercase text-xs tracking-wide">${i.invoice_type}</span></p>
        <p class="text-sm text-slate-600 dark:text-slate-300">Izrakstīts: ${i.issue_date} · Termiņš: ${i.due_date}</p>
        <p class="text-sm text-slate-700 dark:text-slate-200">Klients: ${i.client_name} · Izsniedzējs: ${i.seller_name}</p>
        <p class="text-sm"><b>Kopā:</b> ${i.total} EUR · <b>Apmaksājams:</b> ${i.payable} EUR</p>
      </div>
      <a class="text-blue-600 underline flex items-center gap-1" href="/api/invoices/${i.id}/pdf"><i data-lucide="download"></i> PDF</a>
    </div>
  `).join('');
  renderIcons();
}

async function loadNotes() {
  const data = await fetch('/api/delivery-notes').then(r => r.json());
  noteList.innerHTML = data.map(n => `
    <div class="border border-slate-700 rounded p-2 flex items-center justify-between">
      <span>${n.number} · ${n.issue_date} · ${n.receiver_name}</span>
      <a class="text-indigo-300 underline" href="/api/delivery-notes/${n.id}/pdf">PDF</a>
    </div>
  `).join('');
}

function setupMenuTabs() {
  const buttons = Array.from(document.querySelectorAll('.menu-item'));
  const tabs = Array.from(document.querySelectorAll('.tab-panel'));

  function activate(tabId) {
    tabs.forEach(t => t.classList.toggle('hidden', t.id !== tabId));
    buttons.forEach(b => {
      const active = b.dataset.tab === tabId;
      b.classList.toggle('bg-indigo-600/30', active);
      b.classList.toggle('border', active);
      b.classList.toggle('border-indigo-400/50', active);
    });
  }

  buttons.forEach(b => b.addEventListener('click', () => activate(b.dataset.tab)));
  activate('tab-invoices');
}

openInvoiceFormBtn.addEventListener('click', () => {
  invoiceFormCard.classList.toggle('hidden');
});

typeSelect.addEventListener('change', updateAdvanceFields);
    <div class="border dark:border-slate-700 rounded p-2 flex items-center justify-between">
      <div>
        <p class="font-medium">${n.number}</p>
        <p class="text-sm text-slate-600 dark:text-slate-300">${n.issue_date} · ${n.receiver_name}</p>
      </div>
      <a class="text-blue-600 underline flex items-center gap-1" href="/api/delivery-notes/${n.id}/pdf"><i data-lucide="download"></i> PDF</a>
    </div>
  `).join('');
  renderIcons();
}

filterType.addEventListener('change', loadInvoices);
sortBy.addEventListener('change', loadInvoices);
searchQ.addEventListener('input', loadInvoices);

setupMenuTabs();
hydrateTheme();
updateAdvanceFields();
loadParties();
loadInvoices();
loadNotes();
renderIcons();
