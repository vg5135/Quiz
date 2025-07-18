<template>
  <div class="notes-popover-overlay" @click="closeNotes" v-if="isVisible">
    <div class="notes-popover" @click.stop>
      <!-- Header -->
      <div class="notes-header">
        <div class="header-left">
          <div class="logo-section">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#1976D2"/></svg>
            <h2>Notes</h2>
          </div>
        </div>
        <div class="header-right">
          <button @click="createNewNote" class="add-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/></svg>
          </button>
          <button @click="closeNotes" class="close-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/></svg>
          </button>
        </div>
      </div>
      <div class="notes-content">
        <!-- Sidebar: Notes List -->
        <div class="notes-panel">
          <div class="notes-list">
            <div v-if="notes.length === 0" class="empty-state">
              <p>No notes yet</p>
            </div>
            <div v-else class="notes-items">
              <div v-for="note in notes" :key="note.id" class="note-item" :class="{selected: selectedNote && selectedNote.id === note.id}" @click="selectNote(note)">
                <div class="note-color" :style="{background: note.color || '#ffe082'}"></div>
                <div class="note-title-area">
                  <div class="note-title">{{ note.title }}</div>
                  <div class="note-date">{{ formatDate(note.updated_at) }}</div>
                </div>
                <button @click.stop="deleteNote(note)" class="delete-btn">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM8 9H16V19H8V9ZM15.5 4L14.5 3H9.5L8.5 4H5V6H19V4H15.5Z" fill="currentColor"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- Main Area: Note Editor -->
        <div class="editor-panel">
          <div v-if="!selectedNote" class="no-note-selected">
            <div class="no-note-content">
              <h3>Select a note</h3>
              <p>Choose a note from the list or create a new one to start writing.</p>
            </div>
          </div>
          <div v-else class="note-editor">
            <input v-model="selectedNote.title" @blur="updateNoteTitle" class="note-title-input" placeholder="Note title..." />
            <textarea
              v-model="selectedNote.content"
              @input="updateNoteContent"
              class="note-content-textarea"
              placeholder="Start writing your note here..."
              @contextmenu="showCustomMenu"
            ></textarea>
            <!-- Custom context menu -->
            <div v-if="customMenu.visible" class="context-menu" :style="{ top: customMenu.y + 'px', left: customMenu.x + 'px' }" @mousedown.stop>
              <div class="menu-item" @click="openNotePicker">Hyperlink to Note</div>
            </div>
            <!-- Note picker modal -->
            <div v-if="notePicker.visible" class="note-picker-modal">
              <div class="modal-content">
                <div class="modal-header">
                  <span>Select note to link</span>
                  <button class="close-btn" @click="closeNotePicker">&times;</button>
                </div>
                <div class="modal-list">
                  <div v-for="note in notes.filter(n => n.id !== selectedNote.id)" :key="note.id" class="modal-note-item" @click="pickNoteToLink(note)">
                    {{ note.title }}
                  </div>
                </div>
              </div>
            </div>
            <!-- Render note:// links as clickable with hover preview -->
            <div v-if="selectedNote.content" class="note-content-rendered">
              <span v-for="(part, idx) in parseNoteLinks(selectedNote.content)" :key="idx">
                <template v-if="part.type === 'link'">
                  <a href="#" @click.prevent="selectNoteById(part.noteId)" @mouseenter="showNotePreview(part.noteId, $event)" @mouseleave="hideNotePreview">
                    {{ part.text }}
                  </a>
                </template>
                <template v-else>{{ part.text }}</template>
              </span>
            </div>
            <!-- Note preview popup -->
            <div v-if="previewNote" class="note-preview-popup" :style="{ top: previewPos.y + 'px', left: previewPos.x + 'px' }">
              <h4>{{ previewNote.title }}</h4>
              <pre>{{ previewNote.content }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { getNotes, createNotes, getNotesDetail, updateNotes, deleteNotes } from '../api';

const props = defineProps({
  isVisible: { type: Boolean, default: false }
});
const emit = defineEmits(['close']);

const notes = ref([]);
const selectedNote = ref(null);

const closeNotes = () => emit('close');

const fetchNotes = async () => {
  try {
    const response = await getNotes();
    notes.value = response.notes || [];
    if (notes.value.length && !selectedNote.value) {
      selectedNote.value = notes.value[0];
    }
  } catch (error) {
    console.error('Error fetching notes:', error);
  }
};

const createNewNote = async () => {
  try {
    const response = await createNotes({ title: 'Untitled Note', content: '', color: '#ffe082' });
    await fetchNotes();
    const newNote = notes.value.find(note => note.id === response.notes.id);
    if (newNote) selectNote(newNote);
  } catch (error) {
    console.error('Error creating note:', error);
  }
};

const selectNote = async (note) => {
  try {
    const response = await getNotesDetail(note.id);
    selectedNote.value = response.notes;
  } catch (error) {
    console.error('Error selecting note:', error);
  }
};

const updateNoteTitle = async () => {
  if (!selectedNote.value) return;
  try {
    await updateNotes(selectedNote.value.id, { title: selectedNote.value.title });
    await fetchNotes();
  } catch (error) {
    console.error('Error updating note title:', error);
  }
};

const updateNoteContent = async () => {
  if (!selectedNote.value) return;
  try {
    await updateNotes(selectedNote.value.id, { content: selectedNote.value.content });
  } catch (error) {
    console.error('Error updating note content:', error);
  }
};

const deleteNote = async (note) => {
  if (!confirm('Delete this note?')) return;
  try {
    await deleteNotes(note.id);
    await fetchNotes();
    if (selectedNote.value?.id === note.id) selectedNote.value = notes.value[0] || null;
  } catch (error) {
    console.error('Error deleting note:', error);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
};

// Custom context menu
const customMenu = ref({ visible: false, x: 0, y: 0, selection: '', anchorStart: 0, anchorEnd: 0 });
const showCustomMenu = (e) => {
  const textarea = e.target;
  const selection = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);
  if (selection) {
    e.preventDefault();
    customMenu.value = {
      visible: true,
      x: e.clientX,
      y: e.clientY,
      selection,
      anchorStart: textarea.selectionStart,
      anchorEnd: textarea.selectionEnd
    };
  } else {
    customMenu.value.visible = false;
  }
};
const hideCustomMenu = (e) => {
  if (!e || !e.target || !e.target.closest('.context-menu')) {
    customMenu.value.visible = false;
  }
};

const notePicker = ref({ visible: false });
const openNotePicker = () => {
  notePicker.value.visible = true;
  hideCustomMenu();
};
const closeNotePicker = () => { notePicker.value.visible = false; };
const pickNoteToLink = (note) => {
  const textarea = document.querySelector('.note-content-textarea');
  if (!textarea) return;
  const before = selectedNote.value.content.substring(0, customMenu.value.anchorStart);
  const after = selectedNote.value.content.substring(customMenu.value.anchorEnd);
  const link = `[${customMenu.value.selection}](note://${note.id})`;
  selectedNote.value.content = before + link + after;
  updateNoteContent();
  notePicker.value.visible = false;
  nextTick(() => textarea.focus());
};

onMounted(() => {
  fetchNotes();
  window.addEventListener('note-updated', handleNoteUpdated);
  document.addEventListener('mousedown', hideCustomMenu);
});
onUnmounted(() => {
  window.removeEventListener('note-updated', handleNoteUpdated);
  document.removeEventListener('mousedown', hideCustomMenu);
});

function handleNoteUpdated(e) {
  if (selectedNote.value && selectedNote.value.id === e.detail.id) {
    selectNote(selectedNote.value);
  }
}

// Helper to parse note:// links in content
function parseNoteLinks(content) {
  const regex = /\[([^\]]+)\]\(note:\/\/(\d+)\)/g;
  let lastIndex = 0;
  let match;
  const parts = [];
  while ((match = regex.exec(content)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', text: content.substring(lastIndex, match.index) });
    }
    parts.push({ type: 'link', text: match[1], noteId: Number(match[2]) });
    lastIndex = regex.lastIndex;
  }
  if (lastIndex < content.length) {
    parts.push({ type: 'text', text: content.substring(lastIndex) });
  }
  return parts;
}

// Select note by ID
const selectNoteById = async (id) => {
  const note = notes.value.find(n => n.id === id);
  if (note) await selectNote(note);
};

// Note preview popup
const previewNote = ref(null);
const previewPos = ref({ x: 0, y: 0 });
const showNotePreview = async (id, event) => {
  const resp = await getNotesDetail(id);
  previewNote.value = resp.notes;
  previewPos.value = { x: event.clientX + 10, y: event.clientY + 10 };
};
const hideNotePreview = () => { previewNote.value = null; };
</script>

<style scoped>
.notes-popover-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 24px;
}
.notes-popover {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  width: 90vw;
  max-width: 1100px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.notes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 28px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}
.header-left .logo-section {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-left h2 {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  color: #1a1a1a;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 14px;
}
.add-btn {
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  margin-right: 8px;
  transition: background 0.2s;
}
.add-btn:hover { background: #1565c0; }
.close-btn {
  background: transparent;
  border: none;
  color: #666;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}
.close-btn:hover { background: #f0f0f0; color: #333; }
.notes-content {
  flex: 1;
  display: flex;
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}
.notes-panel {
  width: 90px;
  min-width: 70px;
  max-width: 120px;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
  flex-shrink: 0;
  align-items: center;
  padding-top: 24px;
}
.notes-list {
  flex: 1;
  width: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.empty-state {
  text-align: center;
  color: #888;
  font-size: 14px;
  margin-top: 40px;
}
.notes-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  align-items: center;
}
.note-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 56px;
  cursor: pointer;
  position: relative;
}
.note-item.selected .note-color {
  border: 2px solid #1976d2;
}
.note-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 6px;
  border: 2px solid transparent;
  transition: border 0.2s;
}
.note-title-area {
  display: none;
}
.note-date {
  display: none;
}
.delete-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  color: #ff6b6b;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  z-index: 2;
}
.note-item:hover .delete-btn { opacity: 1; }
.editor-panel {
  flex: 1 1 0%;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  overflow: hidden;
  align-items: center;
  justify-content: center;
}
.no-note-selected {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #888;
}
.no-note-content {
  text-align: center;
  max-width: 320px;
  margin: 0 auto;
}
.note-editor {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 40px 0;
  height: 100%;
}
.note-title-input {
  font-size: 2.2rem;
  font-weight: 700;
  border: none;
  outline: none;
  margin-bottom: 24px;
  background: transparent;
  color: #222;
  padding: 0 0 8px 0;
  border-bottom: 2px solid #e0e0e0;
  transition: border-color 0.2s;
}
.note-title-input:focus { border-bottom: 2px solid #1976d2; }
.note-content-textarea {
  flex: 1 1 0%;
  width: 100%;
  min-height: 300px;
  font-size: 1.1rem;
  border: none;
  outline: none;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  resize: none;
  color: #222;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  margin-bottom: 8px;
}
.note-content-textarea:focus { background: #fff; box-shadow: 0 2px 12px rgba(25,118,210,0.08); }
@media (max-width: 900px) {
  .notes-popover { width: 98vw; height: 95vh; }
  .note-editor { max-width: 98vw; padding: 20px 0; }
}
@media (max-width: 600px) {
  .notes-popover { width: 100vw; height: 100vh; border-radius: 0; }
  .notes-header { padding: 10px 8px; }
  .notes-panel { width: 60px; min-width: 40px; }
  .note-editor { padding: 8px 0; }
  .note-title-input { font-size: 1.2rem; }
  .note-content-textarea { padding: 10px; }
}
.context-menu {
  position: fixed;
  z-index: 2000;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18);
  min-width: 180px;
  padding: 8px 0;
  border: 1px solid #e0e0e0;
}
.menu-item {
  padding: 8px 16px;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.15s;
}
.menu-item:hover {
  background: #f0f8ff;
}
.note-picker-modal {
  position: fixed;
  z-index: 3000;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18);
  min-width: 320px;
  max-width: 90vw;
  padding: 24px;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}
.close-btn {
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
.modal-list {
  max-height: 300px;
  overflow-y: auto;
}
.modal-note-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  font-size: 16px;
}
.modal-note-item:hover {
  background: #f0f8ff;
}
.note-preview-popup {
  position: fixed;
  z-index: 3000;
  background: #fff;
  border: 1px solid #1976d2;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(25,118,210,0.18);
  padding: 16px;
  min-width: 250px;
  max-width: 400px;
  max-height: 300px;
  overflow: auto;
}
.note-preview-popup h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #1976d2;
}
.note-preview-popup pre {
  margin: 0;
  font-size: 14px;
  white-space: pre-wrap;
}
</style> 