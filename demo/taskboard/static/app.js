"use strict";

const form = document.getElementById("task-form");
const input = document.getElementById("task-title");
const statusEl = document.getElementById("status");
const listEl = document.getElementById("task-list");
const emptyEl = document.getElementById("empty");

function setStatus(msg) {
  statusEl.textContent = msg || "";
}

async function api(path, options) {
  let res;
  try {
    res = await fetch(path, options);
  } catch (e) {
    throw new Error("Network error: could not reach the server.");
  }
  if (res.status === 204) return null;
  let data = null;
  try { data = await res.json(); } catch (e) { /* no body */ }
  if (!res.ok) {
    throw new Error((data && data.error) || `Request failed (${res.status}).`);
  }
  return data;
}

function formatDate(s) {
  const d = new Date(s);
  return isNaN(d) ? String(s) : d.toLocaleString();
}

function render(tasks) {
  listEl.textContent = "";
  emptyEl.hidden = tasks.length > 0;
  for (const t of tasks) {
    const li = document.createElement("li");
    if (t.done) li.className = "done";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = !!t.done;
    cb.setAttribute("aria-label", `Mark "${t.title}" as done`);
    cb.addEventListener("change", () => mutate(`/api/tasks/${encodeURIComponent(t.id)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ done: cb.checked }),
    }));

    const body = document.createElement("div");
    body.className = "body";
    const title = document.createElement("span");
    title.className = "title";
    title.textContent = t.title;
    const time = document.createElement("time");
    time.dateTime = t.created_at;
    time.textContent = formatDate(t.created_at);
    body.append(title, time);

    const del = document.createElement("button");
    del.type = "button";
    del.className = "del";
    del.textContent = "Delete";
    del.setAttribute("aria-label", `Delete task: ${t.title}`);
    del.addEventListener("click", () => mutate(`/api/tasks/${encodeURIComponent(t.id)}`, { method: "DELETE" }));

    li.append(cb, body, del);
    listEl.append(li);
  }
}

async function load() {
  try {
    const data = await api("/api/tasks");
    render(data.tasks);
  } catch (e) {
    setStatus(e.message);
  }
}

async function mutate(path, options) {
  setStatus("");
  try {
    await api(path, options);
  } catch (e) {
    setStatus(e.message);
  }
  await load();
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const title = input.value.trim();
  if (!title) {
    setStatus("Please enter a task title.");
    return;
  }
  setStatus("");
  try {
    await api("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    input.value = "";
  } catch (e) {
    setStatus(e.message);
    return;
  }
  await load();
  input.focus();
});

load();
