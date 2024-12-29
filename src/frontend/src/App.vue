<script setup lang="ts">
import { Textarea } from "@/components/ui/textarea";
import { ref, onMounted, computed } from 'vue'
import { Button } from "@/components/ui/button";
import { useColorMode, usePreferredColorScheme } from '@vueuse/core'
import { Sun, Moon, Computer } from 'lucide-vue-next';
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'
import { Toaster } from '@/components/ui/sonner'
import { toast } from 'vue-sonner'

const config = ref('')
const mode = useColorMode()
const theme = computed(() => {
    if (mode.value === 'auto') {
        return usePreferredColorScheme().value === 'dark' ? 'vs-dark' : 'vs-light'
    }
    return mode.value === 'light' ? 'vs-light' : 'vs-dark'
})
const editorOptions = {
    automaticLayout: true,
    formatOnType: true,
    formatOnPaste: true,
}

onMounted(async () => {
    config.value = await fetchConfig()
})

const saveConfig = async () => {
    try {
        const response = await fetch('/api/yaml', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: config.value
            })
        })
        if (!response.ok) {
            throw new Error('保存失败')
        }
        toast('保存成功')
    } catch (error) {
        toast('保存失败')
    }
}

async function fetchConfig() {
    const res = await fetch('/app.yaml')
    return await res.text()
}
</script>
<template>
    <Toaster />
    <div class="flex items-center justify-center w-screen h-screen">
        <div class="flex w-full h-full max-w-7xl flex-col p-4">
            <div class="flex w-full h-[5%] items-center gap-4">
                <Button @click="saveConfig"> 保存 </Button>
                <Button @click="mode = 'light'">
                    <Sun />
                </Button>
                <Button @click="mode = 'dark'">
                    <Moon />
                </Button>
                <Button @click="mode = 'auto'">
                    <Computer />
                </Button>
            </div>
            <div class="flex w-full h-[2%]">
            </div>
            <div class="flex w-full h-[93%]">
                <div class="w-[65%] lg:w-[65%] w-full h-full">
                    <VueMonacoEditor 
                        :value="config" 
                        @update:value="(val) => config = val"
                        language="yaml" 
                        :theme="theme" 
                        :options="editorOptions"
                    />
                </div>
                <div class="w-[5%] h-full lg:block hidden"></div>
                <div class="w-[30%] h-full lg:block hidden">
                    <Textarea v-model="config" class="w-full h-full resize-none opacity-100 " disabled/>
                </div>
            </div>
        </div>
    </div>
</template>
