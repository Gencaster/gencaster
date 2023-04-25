<template>
  <div>
    <p>Hello World! Welcome to the Gencaster Editor.</p>
    <p>Log in to see your graphs:</p>
    <div class="login-wrapper">
      <ElForm
        ref="form"
        class="login-form"
        :model="model"
        :rules="rules"
        @submit.prevent
      >
        <ElFormItem prop="username">
          <ElInput
            v-model="model.username"
            placeholder="Username"
          />
        </ElFormItem>
        <ElFormItem prop="password">
          <ElInput
            v-model="model.password"
            placeholder="Password"
            type="password"
          />
        </ElFormItem>
        <ElFormItem>
          <ElButton
            :color="variables.greenLight"
            class="login-button"
            native-type="submit"
            @click="onSubmit"
          >
            Login
          </ElButton>
        </ElFormItem>
      </ElForm>
    </div>
  </div>
</template>

<script lang="ts" setup>
import variables from "@/assets/scss/variables.module.scss";
import { ref } from "vue";
import { useRouter } from "vue-router";
import type { Ref } from "vue";
import { ElButton, ElForm, ElInput, type ElFormItem } from "element-plus";


const router = useRouter();

router.push("/graph");

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

const onSubmit = () => {
  console.log("submit");
};
</script>
