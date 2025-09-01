const BASE_URL = "http://127.0.0.1:8000"; 
const $ = (sel, ctx=document) => ctx.querySelector(sel);

const els = {
  rows: $("#rows"),
  flash: $("#flash"),
  frm: $("#frm"),
  id: $("#id"),
  name: $("#name"),
  bio: $("#bio"),
  picture: $("#picture"),
  btnRefresh: $("#btn-refresh"),
  btnReset: $("#btn-reset"),
  q: $("#q"),
  btnSearch: $("#btn-search"),
  btnClear: $("#btn-clear"),
};


for (const [k,v] of Object.entries(els)) {
  if (!v) console.warn(`[app] Falta en DOM: ${k}`);
}

let all = []; // cache local





const toast = (msg, ok=true) => {
  els.flash.innerHTML = `<div class="alert ${ok?'ok':'err'}">${msg}</div>`;
  setTimeout(()=> els.flash.innerHTML="", 3000);
};

const formDataToActor = () => ({
  id: Number(els.id.value),
  name: els.name.value.trim(),
  bio: els.bio.value.trim(),
  picture: els.picture.value.trim()
});

const fillForm = a => {
  els.id.value = a.id;
  els.name.value = a.name;
  els.bio.value = a.bio;
  els.picture.value = a.picture;
  els.id.focus();
};

const resetForm = () => {
  els.frm.reset();
  els.id.focus();
};

//APi
async function apiList(){
  const r = await fetch(`${BASE_URL}/acteurs`);
  if(!r.ok) throw new Error(`GET /acteurs → ${r.status}`);
  return await r.json();
}
async function apiGet(id){
  const r = await fetch(`${BASE_URL}/acteur/${id}`);
  if(!r.ok) throw new Error(`GET /acteur/${id} → ${r.status}`);
  return await r.json();
}
async function apiCreate(a){
  const r = await fetch(`${BASE_URL}/acteurs`, {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify(a)
  });
  if(!r.ok){
    const body = await r.text();
    throw new Error(`POST /acteurs → ${r.status} ${body}`);
  }
  return await r.json();
}
async function apiUpdate(id, a){
  const r = await fetch(`${BASE_URL}/acteur/${id}`, {
    method:"PUT",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({ name:a.name, bio:a.bio, picture:a.picture })
  });
  if(!r.ok){
    const body = await r.text();
    throw new Error(`PUT /acteur/${id} → ${r.status} ${body}`);
  }
  return await r.json();
}
async function apiDelete(id){
  const r = await fetch(`${BASE_URL}/acteur/${id}`, { method:"DELETE" });
  if(!r.ok){
    const body = await r.text();
    throw new Error(`DELETE /acteur/${id} → ${r.status} ${body}`);
  }
  return await r.json();
}

// ---------------------------



function escapeHtml(s){return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");}
function escapeAttr(s){return String(s).replaceAll('"',"&quot;");}

function render(list){
  els.rows.innerHTML = "";
  if(!Array.isArray(list) || list.length === 0){
    els.rows.innerHTML = `<tr><td colspan="5" class="muted">Aucun résultat…</td></tr>`;
    return;
  }
  for(const a of list){
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><span class="badge co">${a.id}</span></td>
      <td>${escapeHtml(a.name)}</td>
      <td>${escapeHtml(a.bio)}</td>
      <td><img src="${escapeAttr(a.picture)}" alt="photo" /></td>
      <td>
        <button class="btn" data-act="edit" data-id="${a.id}">Éditer</button>
        <button class="btn" style="background:var(--warn)" data-act="load" data-id="${a.id}">Charger</button>
        <button class="btn" style="background:var(--danger)" data-act="del" data-id="${a.id}">Supprimer</button>
      </td>`;
    els.rows.appendChild(tr);
  }
}

//.---- eventos

// Actualizar
els.btnRefresh.addEventListener("click", async ()=>{
  try{
    all = await apiList();
    render(all);
    toast("Liste actualisée");
  }catch(e){ toast(e.message,false); console.error(e); }
});

// Buscar por ID
els.btnSearch.addEventListener("click", async ()=>{
  const id = Number(els.q.value);
  if(!id){ render(all); return; }
  try{
    const a = await apiGet(id);
    render([a]);
    toast(`Acteur #${id} trouvé`);
  }catch(e){
    render([]);
    toast(`Acteur #${id} introuvable`, false);
    console.error(e);
  }
});
els.q.addEventListener("keydown", (ev)=>{
  if(ev.key === "Enter"){ ev.preventDefault(); els.btnSearch.click(); }
});

// Limpiar filtro
els.btnClear.addEventListener("click", ()=>{
  els.q.value = "";
  render(all);


});

// Acciones en la tabla



els.rows.addEventListener("click", async (ev)=>{
  const btn = ev.target.closest("button[data-act]");
  if(!btn) return;
  const id = Number(btn.dataset.id);
  const act = btn.dataset.act;

  if(act === "edit"){
    const a = all.find(x => x.id === id);
    if(a) fillForm(a);
    return;
  }

  if(act === "load"){
    try{
      const a = await apiGet(id);
      fillForm(a);
      toast(`Acteur ${id} chargé`);
    }catch(e){ toast(e.message,false); console.error(e); }
    return;
  }



  if(act === "del"){
    if(!confirm(`Supprimer l’acteur ${id} ?`)) return;
    try{
      await apiDelete(id);
      all = await apiList(); // sincroniza con backend
      render(all);
      toast(`Acteur ${id} supprimé`);
    }catch(e){ toast(e.message,false); console.error(e); }
  }
});

// Crear- Actualizar
els.frm.addEventListener("submit", async (ev)=>{
  ev.preventDefault();
  const a = formDataToActor();
  if(!a.id || !a.name || !a.bio || !a.picture){
    toast("Champs obligatoires manquants", false); return;
  }
  try{


    // existe ya en la lista?
    const exists = all.some(x => x.id === a.id);
    if(exists){
      await apiUpdate(a.id, a);
      toast(`Acteur ${a.id} mis à jour`);
    }else{
      await apiCreate(a);
      toast(`Acteur ${a.id} créé`);
    }



    all = await apiList(); // sincroniza con backend JSON
    render(all);
    resetForm();
  }catch(e){
    toast(e.message,false);
    console.error(e);
  }
});




(async function boot(){
  try{
    all = await apiList();
    render(all);
    console.log("[app] initial list:", all);
  }catch(e){ toast(e.message,false); console.error(e); }
})();
