<script setup lang="ts">
import { useLoginUserMutation } from '@/graphql';
import { useInterfaceStore } from '@/stores/InterfaceStore';
import { ElMessage, type FormInstance } from 'element-plus';
import { storeToRefs } from 'pinia';
import { reactive, ref, type Ref } from 'vue';

const loginForm = reactive({
  username: '',
  password: '',
});

const {user} = storeToRefs(useInterfaceStore());

const loginFormRef: Ref<FormInstance | undefined> = ref();

const loginMutation = useLoginUserMutation();

const runLogin: Ref<boolean> = ref(false);

const tryLogin = async () => {
  runLogin.value = true;
  const { data, error } = await loginMutation.executeMutation({
    username: loginForm.username,
    password: loginForm.password,
  });
  runLogin.value = false;
  if (error) {
    ElMessage.error(`Unexpected error on login: ${error.message}`);
    return;
  }
  if (data?.authLogin) {
    if(data.authLogin.__typename === 'LoginError') {
        ElMessage.error(`Benutzername / Password stimmen nicht überein`);
        loginFormRef.value?.resetFields();
        return;
    }
    showLoginScreen.value = false;
    ElMessage.success(`Erfolgreich angemeldet`);
    user.value = data.authLogin;
  }
};

const showLoginScreen = ref<boolean>(true);
</script>

<template>
  <div class="login-form">
    <ElDialog
      v-model="showLoginScreen"
      title="Bitte einloggen"
      width="40%"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <ElForm
        ref="loginFormRef"
        v-loading="runLogin"
        :model="loginForm"
        label-width="40%"
        @submit.prevent="tryLogin"
      >
        <ElFormItem
          label="Benutzername"
          prop="username"
        >
          <ElInput
            v-model="loginForm.username"
            @keyup.enter="tryLogin"
          />
        </ElFormItem>
        <ElFormItem
          label="Passwort"
          prop="password"
        >
          <ElInput
            v-model="loginForm.password"
            show-password
            type="password"
            @keyup.enter="tryLogin"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton disabled>Passwort vergessen</ElButton>
          <ElButton
            type="primary"
            @click="tryLogin()"
          > Login </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
