<template>
  <router-view />
  <Chatbot />
  <ContextMenu
    :visible="contextMenu.visible"
    :x="contextMenu.x"
    :y="contextMenu.y"
    :notes="notes"
    :contentToAdd="contextMenu.content"
    @add-to-note="handleAddToNote"
  />
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import Chatbot from './components/Chatbot.vue';
import ContextMenu from './components/ContextMenu.vue';
import { getNotes, updateNotes, getNotesDetail } from './api';

const notes = ref([]);
const contextMenu = ref({ visible: false, x: 0, y: 0, content: '' });

const fetchNotes = async () => {
  try {
    const response = await getNotes();
    notes.value = response.notes || [];
  } catch (e) {
    notes.value = [];
  }
};

const handleAddToNote = async (note, content) => {
  if (!note || !content) return;
  const detailResp = await getNotesDetail(note.id);
  const latestNote = detailResp.notes;
  const newContent = (latestNote.content || '') + '\n' + content;
  const data = { content: newContent };
  await updateNotes(note.id, data);
  contextMenu.value.visible = false;
  await fetchNotes();
  window.dispatchEvent(new CustomEvent('note-updated', { detail: { id: note.id } }));
};

const hideContextMenu = () => {
  contextMenu.value.visible = false;
};

const onContextMenu = async (e) => {
  let content = '';
  // If image
  if (e.target && e.target.tagName === 'IMG') {
    content = `![Image](${e.target.src})`;
  } else {
    // If text selected
    const selection = window.getSelection();
    if (selection && selection.toString().trim()) {
      content = selection.toString();
    }
  }
  if (content) {
    e.preventDefault();
    await fetchNotes();
    contextMenu.value = {
      visible: true,
      x: e.clientX,
      y: e.clientY,
      content
    };
  } else {
    hideContextMenu();
  }
};

onMounted(() => {
  document.addEventListener('contextmenu', onContextMenu);
  document.addEventListener('click', hideContextMenu);
});
</script>

<style>
body {
  margin: 0;
  font-family: "Inter", "Segoe UI", Arial, sans-serif;
  background: #f7fafc;
}
#app{
  margin:0 !important;
  padding:0 !important;
}
</style>
