<template lang="pug">

transition
    .menu(v-if="active")
        .nav
            .link.favorites(@click="goTo({ name: 'favorites' })") Избранное 
                .favorites-count ({{ favorites }})
            .link(v-for="(link, index) in links" :key="index" @click="goTo(link.link)") {{ link.text }}
        .options
            .order Оставить заявку
            .social
                a.social-link(:href="contacts.instagram" tagret="_blank")
                    g-icon(name="ui/instagram")
                a.social-link(:href="contacts.telegram" tagret="_blank")
                    g-icon(name="ui/telegram")

</template>
<script>
export default {
    props: {
        active: Boolean
    },
    data: () => ({
        links: [
            {
                text: 'Главная',
                link: { name: 'main' }
            },
            {
                text: 'Поиск по параметрам',
                link: { name: 'catalog', query: { view: 'list' } }
            },
            {
                text: 'Поиск по карте',
                link: { name: 'catalog', query: { view: 'map' } }
            },
            {
                text: 'О нас',
                link: { name: 'main' }
            },
        ]
    }),
    computed: {
        favorites() {
            return this.$store.state.catalog.favorites.length
        },
        contacts() {
            return this.$store.state.content.contacts
        },
    },
    methods: {
        goTo(link) {
            this.$router.push(link)
            this.$emit('close')
        }
    }
}
</script>
<style lang="stylus" scoped>

@keyframes menuShow
    0%
        transform translate(-100%)
    100%
        transform translate(0)

.menu
    &.v-enter-active
        animation menuShow .2s
    &.v-leave-active
        animation menuShow .2s reverse
        
    display none
    +$phone()
        display flex

    position fixed
    background-color #fff
    bottom 0
    left 0
    right 0
    top 54px
    flex-direction column

    padding-top 36px
    padding-left 30px
    padding-bottom 30px
    padding-right 16px
    justify-content space-between

.nav
    padding-left 30px
    .link
        display flex
        font-size 18px
        font-weight 500
        line-height 22px
        cursor pointer
        margin-top 24px
        &:first-child
            margin-top 0
        &.favorites
            padding-bottom 16px
            border-bottom 1px solid $gray2
            .favorites-count
                margin-left .5em
                color $primary

.options
    display flex
    justify-content space-between
    align-items center
    .order
        $btn('border')
    
    .social
        display flex
        &-link
            font-size 24px
            padding 8px

</style>
