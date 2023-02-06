<template>
  <div>
    <p>Hello World! Welcome to the Gencaster Editor.</p>
    <p>Log in to see your graphs:</p>
    <div class="login-wrapper">
      <el-form ref="form" class="login-form" :model="model" :rules="rules" @submit.prevent>
        <el-form-item prop="username">
          <el-input v-model="model.username" placeholder="Username" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="model.password" placeholder="Password" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button ref="submitBtn" :color="variables.greenLight" class="login-button" native-type="submit" @click="onSubmit">
            Login
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useNuxtApp } from "#app";
import * as variables from "@/assets/scss/variables.module.scss";
const nuxtApp = useNuxtApp();

// Store
const graphsStore = nuxtApp.graphsStore;
const { graphs } = storeToRefs(graphsStore);

// Composables
const router = useRouter();

const form = ref<HTMLElement>();

const model = ref({
  username: "",
  password: ""
});

const rules = ref({
  username: [
    {
      required: true,
      message: "Username is required",
      trigger: "blur"
    },
    {
      min: 4,
      message: "Username length should be at least 5 characters",
      trigger: "blur"
    }
  ],
  password: [
    { required: true, message: "Password is required", trigger: "blur" },
    {
      min: 5,
      message: "Password length should be at least 5 characters",
      trigger: "blur"
    }
  ]
});

watch(graphs, () => {
  // reroute if data incoming
  router.push({
    path: "/graphs"
  });
});

const onSubmit = () => {
  console.log("submit");
};
</script>
