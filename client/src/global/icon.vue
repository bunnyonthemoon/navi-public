<template lang="pug">

component.icon.g-icon(:is="icon")

</template>
<script>
import { defineAsyncComponent } from 'vue'
export default {
    props: {
        name: {
            required: true,
            type: String
        }
    },
    computed: {
        icon() {
            return defineAsyncComponent(() => import('@/assets/icons/' + this.name + '.svg?inline'))
        }
    }
}
</script>
