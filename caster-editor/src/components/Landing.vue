<template>
  <div>
    <p>Hello World! Welcome to the GenCaster Editor.</p>
    <p>Log in to see your graphs:</p>
    <input v-model="model.username">
    <div class="login-wrapper">
      <el-form
        ref="form"
        class="login-form"
        :model="model"
        :rules="rules"
        @submit.prevent
      >
        <el-form-item prop="username">
          <el-input
            v-model="model.username"
            placeholder="Username"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="model.password"
            placeholder="Password"
            type="password"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            :color="variables.greenLight"
            class="login-button"
            native-type="submit"
            @click="onSubmit"
          >
            Login
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import variables from "@/assets/scss/variables.module.scss";
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import type { Ref } from "vue";
import { useGraphsStore } from "@/stores/GraphsStore";

// Store
const { graphs } = storeToRefs(useGraphsStore());
const router = useRouter();

const form: Ref<HTMLElement | undefined> = ref(undefined);

interface LoginModel {
  username: string;
  password: string;
}

const model: Ref<LoginModel> = ref({ username: "", password: "" });

const rules = ref({
  username: [
    {
      required: true,
      message: "Username is required",
      trigger: "blur",
    },
    {
      min: 4,
      message: "Username length should be at least 5 characters",
      trigger: "blur",
    },
  ],
  password: [
    { required: true, message: "Password is required", trigger: "blur" },
    {
      min: 5,
      message: "Password length should be at least 5 characters",
      trigger: "blur",
    },
  ],
});

watch(graphs, () => {
  // @todo create a log-in state
  router.push("/graphs");
});

const onSubmit = () => {
  console.log("submit");
};
</script>
