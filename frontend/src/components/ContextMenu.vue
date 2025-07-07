<template>
  <div v-if="visible" class="context-menu" :style="{ top: y + 'px', left: x + 'px' }">
    <div class="menu-title">Add to Notes</div>
    <div v-if="notes.length === 0" class="menu-empty">No notes found</div>
    <div v-else class="menu-list">
      <div v-for="note in notes" :key="note.id" class="menu-item" @click="$emit('add-to-note', note, contentToAdd)">
        <span class="note-dot" :style="{ background: note.color || '#ffe082' }"></span>
        {{ note.title }}
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  visible: Boolean,
  x: Number,
  y: Number,
  notes: Array,
  contentToAdd: String
});
const emit = defineEmits(['add-to-note']);
</script>

<style scoped>
.context-menu {
  position: fixed;
  z-index: 2000;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18);
  min-width: 180px;
  padding: 8px 0;
  border: 1px solid #e0e0e0;
  animation: fadeIn 0.15s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to   { opacity: 1; transform: scale(1); }
}
.menu-title {
  font-size: 14px;
  font-weight: 600;
  padding: 8px 16px 4px 16px;
  color: #1976d2;
}
.menu-empty {
  padding: 8px 16px;
  color: #888;
  font-size: 13px;
}
.menu-list {
  display: flex;
  flex-direction: column;
}
.menu-item {
  padding: 8px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  transition: background 0.15s;
}
.menu-item:hover {
  background: #f0f8ff;
}
.note-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}
</style> 