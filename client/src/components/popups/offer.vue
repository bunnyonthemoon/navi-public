<template lang="pug">

.offer
    .close(@click="$emit('close')")
        g-icon(name="ui/close")
    .offer-head
        .adobe
            g-icon(name="ui/adobe")
        .title {{ type == 'private' ? 'Получить специальное предложение' : 'Оставить заявку' }}
    form.form(@submit.prevent="submit")
        input.input(v-model="name" placeholder="Имя" required)
        input.input(v-model="email" placeholder="e-mail" type="email" required)
        button.submit(type="submit" :class="{ loading: status == 'loading', 'loading-success': status == 'success', 'loading-error': status == 'error' }") {{ type == 'private' ? 'Получить предложение' : 'Оставить заявку' }}
    .agreement Нажимая на кнопку «{{ type == 'private' ? 'Получить предложение' : 'Оставить заявку' }}» вы соглашаетесь с  
        a(:href="$store.state.content.files.agreement" target="_blank") пользовательским соглашением

</template>
<script>
import axios from 'axios'
export default {
    props: {
        query: String
    },
    data: (context) => ({
        name: null,
        email: null,
        type: context.query.split('|')[0],
        id: context.query.split('|')[1],
        status: null
    }),
    methods: {
        async submit() {
            this.status = 'loading'
            const { data } = await axios.post('/api/auth/offer/', {
                name: this.name,
                email: this.email,
                id: this.id,
                type: this.type
            })
            if (data.status === true)
                this.status = 'success'
            else this.status = 'error'
            
            setTimeout(() => this.status = null, 5000)
        }
    }
}
</script>
<style lang="stylus" scoped>

.popup.offer
    width 430px
    padding 0
    border-radius 25px
    +$phone()
        width 100%
        border-radius 0
    .close
        color #fff
        top 15px
        right 15px
        font-size 30px

.form
    display flex
    flex-direction column

.offer-head
    background-image url('~images/ui/popup-offer.jpg')
    background-size cover
    background-position center
    color #fff
    display flex
    flex-direction column
    align-items center
    justify-content center
    padding 80px 40px 20px
    position relative
    text-align center
    +$phone()
        padding 60px 40px 20px
    &::after
        content ''
        position absolute
        width 100%
        height 110px
        bottom 0
        left 0
        background linear-gradient(0deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%)
    .icon
        color #fff
        fill #fff
        stroke #fff
        z-index 2
        position relative
        font-size 46px
        &:deep()
            rect
                fill none

    .title
        z-index 2
        position relative
        font-size 28px
        line-height 34px
        font-weight 500
        +$phone()
            font-size 23px
            line-height 28px

.form
    padding 40px 60px 0
    +$phone()
        padding 40px 40px 0
    .input
        height 50px
        width 100%
        border 1px solid $gray
        padding 0 12px
        margin-top 23px
        &:first-child
            margin-top 0
.submit
    $btn('secondary')
    margin-top 23px
    height 40px

.agreement
    padding 30px 50px
    text-align center
    font-size 14px
    color $gray
    a
        color $primary
        cursor pointer

</style>
