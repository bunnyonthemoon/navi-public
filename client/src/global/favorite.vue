<template lang="pug">

.g-favorite(:class="{ active }" @click="active = !active")
    g-icon(name="ui/favorite")

</template>
<script>
export default {
    props: {
        id: Number
    },
    computed: {
        active: {
            get() {
                return this.$store.state.catalog.favorites.indexOf(this.id) != -1
            },
            set(value) {
                if (value && !this.active)
                    this.$store.dispatch('catalog/favorite', { id: this.id, action: 'add' })
                if (!value && this.active)
                    this.$store.dispatch('catalog/favorite', { id: this.id, action: 'remove' })
            }
        }
    }
}
</script>
