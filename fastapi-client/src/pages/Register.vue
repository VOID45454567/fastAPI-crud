<template>
  <div class="form">
    <div class="form-control">
      <label for="login">login</label>
      <input type="text" placeholder="login" v-model="login" />
    </div>
    <div class="form-control">
      <label for="email">email</label>
      <input type="text" placeholder="email" v-model="email" />
    </div>
    <button @click="sendData">submit</button>
  </div>
</template>
<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
const authStore = useAuthStore();

const login = ref<string>("");
const email = ref<string>("");

const sendData = async () => {
  await authStore.register(login.value, email.value);
};
</script>
