<template lang="pug">

router-view.layout

</template>
<script>
export default {
    async beforeCreate() {
		await this.$store.dispatch('init')
	},
}
</script>
