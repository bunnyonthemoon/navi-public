<template lang="pug">

.g-share(v-if="supportsShare" @click="share")
    g-icon(name="ui/share")

</template>
<script>
export default {
    props: {
        id: [String, Number]
    },
    computed: {
        supportsShare() {
            return navigator.share ? true : false
        }
    },
    methods: {
        async share() {
            try {
                await navigator.share({
                    url: `${window.location.origin}/complex/${this.id}`
                })
            } catch(error) {
                console.log(error)
            }
        }
    }
}
</script>
