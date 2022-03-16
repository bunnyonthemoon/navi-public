<template lang="pug">

.head
    h1.name {{ complex.name }}
    .address {{ complex.address }}

</template>
<script>
export default {
    props: {
        complex: Object
    },
}
</script>
<style lang="stylus" scoped>

.head
    position relative
    margin-bottom 30px
    +$phone()
        display none

.name
    $h1()

.address
    color #7A848B

.options
    position absolute
    right 0
    bottom 0
    display flex
    color #434343

.share
    margin-right 24px

</style>
