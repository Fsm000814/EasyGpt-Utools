<template>
  <div class="context">
    <div class="header">
      <input
        type="text"
        v-model="searchQuery"
        class="search-input"
        placeholder="Search templates..."
      />
      <button class="create-btn" @click="createTemplate">
        Create Template
      </button>
    </div>
    <div class="template-grid">
      <div
        v-for="template in filteredTemplates"
        :key="template.id"
        class="template-item"
        @click="selectTemplate(template)"
      >
        {{ template.name }}
      </div>
    </div>
    <div v-if="selectedTemplate" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2>{{ selectedTemplate.name }}</h2>
        <p>// ...其他模板信息...</p>
        <button class="modal-close-btn" @click="closeModal">Close</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'template-configuration',
  data() {
    return {
      searchQuery: '',
      templates: [
        { id: 1, name: 'Template 1' },
        { id: 2, name: 'Template 2' },
        // More template objects...
      ],
      selectedTemplate: null,
    };
  },
  computed: {
    filteredTemplates() {
      if (this.searchQuery) {
        return this.templates.filter((template) =>
          template.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      return this.templates;
    },
  },
  methods: {
    searchTemplates() {
      // Implement search logic
      console.log('Searching for:', this.searchQuery);
    },
    createTemplate() {
      // Implement create template logic
      console.log('Creating a new template');
    },
    selectTemplate(template) {
      this.selectedTemplate = template;
    },
    closeModal() {
      this.selectedTemplate = null;
    },
  },
};
</script>

<style>
.context {
  padding: 100px;
}
/* Header/search/create section styles */
.header {
  display: flex;
  gap: 15px; /* Add space between items */
  margin-bottom: 30px;
}

.search-input,
.search-btn,
.create-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
}

.search-input {
  flex-grow: 1; /* Input takes available space */
  border: 1px solid #dfe1e5;
}

.search-btn,
.create-btn {
  cursor: pointer;
  background-color: #1a73e8;
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.search-btn:hover,
.create-btn:hover {
  background-color: #1558b3;
}

/* Template grid styles */
.template-grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    minmax(200px, 1fr)
  ); /* Responsive grid */
  gap: 20px; /* Add space between grid items */
}

.template-item {
  padding: 20px;
  background-color: #e6f0fa;
  color: #333;
  text-align: center;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.template-item:hover {
  /* Hover state styles */
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  width: 500px; /* Set a fixed width for the modal */
  max-width: 95%; /* Ensure modal is not too wide on small screens */
}

.modal-close-btn {
  display: block;
  margin-top: 20px;
  border: none;
  background-color: #1a73e8;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.modal-close-btn:hover {
  background-color: #1558b3;
}

/* Add your additional custom styles below */
</style>
