<template>
  <div class="dashboard-container">
    <header class="header">
      <div class="header-content">
        <h1 class="logo">Tasks<span>.</span></h1>
        <div class="user-profile">
          <span class="user-email">{{ user?.email }}</span>
          <!-- В будущем здесь может быть кнопка Logout -->
        </div>
      </div>
    </header>

    <main class="main-content">
      <!-- Секция создания задачи -->
      <section class="create-section">
        <h2 class="section-title">Create new task</h2>
        <form class="task-form" @submit.prevent="handleCreate">
          <div class="form-group">
            <input
              v-model="newTask.title"
              type="text"
              placeholder="Task title"
              required
              class="geist-input title-input"
            />
            <input
              v-model="newTask.description"
              type="text"
              placeholder="Description (optional)"
              class="geist-input"
            />
          </div>

          <div class="form-row">
            <select v-model="newTask.priority" class="geist-input select-input">
              <option :value="1">High Priority</option>
              <option :value="2">Medium Priority</option>
              <option :value="3">Low Priority</option>
            </select>

            <input v-model="newTask.dueDate" type="date" class="geist-input" />

            <button
              type="submit"
              class="btn-primary"
              :disabled="tasksStore.loading"
            >
              {{ tasksStore.loading ? "Creating..." : "Add Task" }}
            </button>
          </div>
        </form>
        <p v-if="tasksStore.error" class="error-msg">{{ tasksStore.error }}</p>
      </section>

      <!-- Секция списка задач -->
      <section class="tasks-section">
        <div class="section-header">
          <h2 class="section-title">My Tasks</h2>
          <span class="task-count">{{ tasksStore.myTasks.length }}</span>
        </div>

        <div
          v-if="tasksStore.loading && tasksStore.myTasks.length === 0"
          class="loading-state"
        >
          Loading tasks...
        </div>

        <div v-else-if="tasksStore.myTasks.length === 0" class="empty-state">
          No tasks yet. Create your first one above.
        </div>

        <div v-else class="tasks-grid">
          <div
            v-for="task in tasksStore.myTasks"
            :key="task.id"
            class="task-card"
            :class="`status-${task.status}`"
          >
            <div class="task-main">
              <div class="task-header">
                <h3 class="task-title">{{ task.title }}</h3>
                <div class="task-badges">
                  <span class="badge status-badge">{{
                    formatStatus(task.status)
                  }}</span>
                  <span class="badge priority-badge">P{{ task.priority }}</span>
                </div>
              </div>

              <p v-if="task.description" class="task-desc">
                {{ task.description }}
              </p>

              <div class="task-meta">
                <span v-if="task.due_date" class="due-date">
                  Due: {{ formatDate(task.due_date) }}
                </span>
              </div>
            </div>

            <button
              @click="handleDelete(task.id)"
              class="btn-delete"
              title="Delete task"
            >
              ✕
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from "vue";
import { useAuthStore } from "@/stores/auth";
import type { User } from "@/types/User";
import { useTasksStore } from "@/stores/task";

const authStore = useAuthStore();
const tasksStore = useTasksStore();

const user = computed(() => authStore.currentUser as User);

const newTask = reactive({
  title: "",
  description: "",
  priority: 3,
  dueDate: new Date().toISOString().split("T")[0], // YYYY-MM-DD
});

onMounted(async () => {
  await tasksStore.getMyTasks();
});

const handleCreate = async () => {
  if (!newTask.title.trim()) return;

  await tasksStore.createTask(
    newTask.title,
    newTask.description,
    "todo", // По умолчанию
    Number(newTask.priority),
    new Date(newTask.dueDate!),
  );

  if (!tasksStore.error) {
    // Сброс формы
    newTask.title = "";
    newTask.description = "";
    newTask.priority = 3;
  }
};

const handleDelete = async (id: number) => {
  await tasksStore.deleteTask(id);
};

// Утилиты форматирования
const formatStatus = (status: string) => {
  const map: Record<string, string> = {
    todo: "To Do",
    in_progress: "In Progress",
    completed: "Completed",
  };
  return map[status] || status;
};

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
};
</script>

<style scoped>
/* 
  Дизайн-система Vercel / Geist 
  - Тени вместо границ
  - Агрессивный letter-spacing
  - Строгая типографика 
*/

.dashboard-container {
  font-family:
    "Geist",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Helvetica,
    Arial,
    sans-serif;
  color: #171717;
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  box-shadow: rgba(0, 0, 0, 0.08) 0px -1px 0px 0px inset; /* Тень-граница снизу */
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.96px;
  margin: 0;
  color: #171717;
}

.logo span {
  color: #0072f5;
}

.user-profile {
  font-size: 14px;
  font-weight: 500;
  color: #4d4d4d;
}

/* Main Content */
.main-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 48px 24px;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 64px;
}

/* Typography */
.section-title {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.96px;
  margin: 0 0 24px 0;
  color: #171717;
}

/* Секция создания */
.create-section {
  display: flex;
  flex-direction: column;
}

.task-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #ffffff;
  padding: 24px;
  border-radius: 8px;
  /* Полная тень карточки Vercel */
  box-shadow:
    rgba(0, 0, 0, 0.08) 0px 0px 0px 1px,
    rgba(0, 0, 0, 0.04) 0px 2px 2px,
    #fafafa 0px 0px 0px 1px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* Inputs */
.geist-input {
  font-family: inherit;
  font-size: 14px;
  color: #171717;
  background: #ffffff;
  padding: 10px 12px;
  border: none;
  border-radius: 6px;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
  transition: box-shadow 0.2s ease;
}

.geist-input::placeholder {
  color: #808080;
}

.geist-input:focus {
  box-shadow:
    rgba(0, 0, 0, 0.08) 0px 0px 0px 1px,
    0 0 0 2px hsla(212, 100%, 48%, 1); /* Focus ring */
}

.title-input {
  font-size: 16px;
  font-weight: 500;
}

.select-input {
  cursor: pointer;
  width: auto;
  min-width: 150px;
}

/* Buttons */
.btn-primary {
  font-family: inherit;
  background: #171717;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.8;
}

.btn-primary:disabled {
  background: #808080;
  cursor: not-allowed;
}

.error-msg {
  color: #ff5b4f; /* Ship Red */
  font-size: 14px;
  margin-top: 12px;
  font-weight: 500;
}

/* Секция списка задач */
.tasks-section {
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.section-header .section-title {
  margin: 0;
}

.task-count {
  background: #fafafa;
  color: #4d4d4d;
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 9999px;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}

.tasks-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Карточка задачи */
.task-card {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #ffffff;
  padding: 20px 24px;
  border-radius: 8px;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
  transition: box-shadow 0.2s ease;
}

.task-card:hover {
  box-shadow:
    rgba(0, 0, 0, 0.08) 0px 0px 0px 1px,
    rgba(0, 0, 0, 0.04) 0px 2px 4px;
}

.task-main {
  flex: 1;
}

.task-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.task-title {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.32px;
  margin: 0;
  color: #171717;
}

.task-desc {
  font-size: 14px;
  color: #4d4d4d;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.task-meta {
  font-size: 12px;
  color: #808080;
  font-weight: 500;
}

/* Бейджи */
.task-badges {
  display: flex;
  gap: 8px;
}

.badge {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 9999px;
}

/* Используем цвета workflow из гайда */
.status-todo .status-badge {
  background: #ebf5ff;
  color: #0a72ef; /* Develop Blue */
}

.status-in_progress .status-badge {
  background: #fdf2f8;
  color: #de1d8d; /* Preview Pink */
}

.status-completed .status-badge {
  background: #fff0ee;
  color: #ff5b4f; /* Ship Red */
}

.priority-badge {
  background: #fafafa;
  color: #171717;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}

/* Кнопка удаления */
.btn-delete {
  background: transparent;
  color: #808080;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn-delete:hover {
  background: #fafafa;
  color: #ff5b4f;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}

/* Состояния */
.loading-state,
.empty-state {
  font-size: 14px;
  color: #808080;
  padding: 32px;
  text-align: center;
  background: #fafafa;
  border-radius: 8px;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}

/* Адаптив */
@media (max-width: 600px) {
  .form-row {
    flex-direction: column;
    align-items: stretch;
  }

  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
