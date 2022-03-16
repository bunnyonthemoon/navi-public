<template lang="pug">

.location
    .g-h2 Жилые комплексы рядом
            
    GMapMap.map(:center="complex.coordinates" :zoom="15" ref="map" :options="mapOptions")
        GMapMarker(:position="complex.coordinates" :icon="mapIcon")

        GMapCluster.catalog-map-cluster(:zoomOnClick="true" :styles="[{ width: 40, height: 40 }]")

            GMapMarker.catalog-map-marker2(v-for="item in around" :key="item.id" :position="item.coordinates" :optimized="false" :label="{ text: `от ${parseInt(item.min_price / 10**6)} млн`, className: 'catalog-map-marker' }" :icon="mapIconAround" @click="opened = item.id")

                GMapInfoWindow.catalog-map-window(:opened="item.id == opened" :closeclick="false")
                    router-link.catalog-map-window-inner(:to="{ name: 'complex', params: { id: item.key } }")
                        .options
                            .favorite
                                g-icon(name="ui/favorite")
                            .close(@click.stop.prevent="opened = null")
                                g-icon(name="ui/close")
                        .img(:style="{ backgroundImage: `url(${item.image})` }")
                        .info
                            .name {{ item.name }}

</template>
<script>
export default {
    props: {
        complex: Object,
        around: Array
    },
    data: () => ({
        mapOptions: {
            zoomControl: true,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            rotateControl: false,
            gestureHandling: 'greedy',
            styles: [
                {
                    "featureType": "all",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "weight": "2.00"
                        }
                    ]
                },
                {
                    "featureType": "all",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        {
                            "color": "#9c9c9c"
                        }
                    ]
                },
                {
                    "featureType": "all",
                    "elementType": "labels.text",
                    "stylers": [
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "all",
                    "stylers": [
                        {
                            "color": "#f2f2f2"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "landscape.man_made",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "all",
                    "stylers": [
                        {
                            "saturation": -100
                        },
                        {
                            "lightness": 45
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#eeeeee"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#7b7b7b"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "simplified"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.icon",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": [
                        {
                            "color": "#46bcec"
                        },
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#c8d7d4"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#070707"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                }
            ],
        },
        mapIcon: {
            url: require('@/assets/icons/ui/map-marker.svg'),
            scaledSize: {width: 38, height: 38},
            labelOrigin: {x: 19, y: 38}
        },
        mapIconAround: {
            url: require('@/assets/icons/ui/empty.svg'),
            // url: null,
            scaledSize: {width: 100, height: 40},
            labelOrigin: {x: 50, y: 0}
        },
        opened: null
    })
}
</script>
<style lang="stylus" scoped>

.location
    margin-top 60px

.around
    margin-top 24px
    max-height 4em
    display inline-flex
    flex-wrap wrap
    flex-direction column
    &-item
        display inline-flex
        justify-content space-between
        width 200px
        margin-top 1em
        margin-left 50px
        &:nth-child(2n+1)
            margin-top 0
        &:nth-child(1), &:nth-child(2)
            margin-left 0
        .time
            font-weight 500

.g-h2
    +$phone()
        padding 0 16px

.map
    height 305px
    width 100%
    margin-top 30px
    +$phone()
        height 250px
    &:deep()
        .gm-style-iw-d
            max-height none!important
        .gm-style-iw
            padding 0
        .cluster
            background-color $secondary
            box-shadow 1px 3px 5px 0 rgba(#000, .15)
            border-radius 100%
            position absolute
            width 40px!important
            height 40px!important
            img
                display none
            span
                color #fff
                font-family $main-font
                font-weight 500
                font-size 20px
                line-height 40px
        .catalog-map-cluster
            background-color red
            display none
        .catalog-map-marker
            background-color #28709E
            cursor pointer
            font-size 13px!important
            font-weight 500
            padding 3px 10px!important
            border-radius 10px
            color #fff!important
            transform translateY(50%)
            font-family $main-font
        .catalog-map-window
            width 180px
            font-family $main-font
            position relative
            box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.15)
            .img
                height 100px
                width 100%
                background-size cover
            .name
                font-size 14px
                line-height 18px
            .info
                padding 8px
            .options
                position absolute
                z-index 10
                top 5px
                right 5px
                display flex
                color #fff
                .favorite
                    margin-right 7px
                    font-size 23px
                    display flex
                .close
                    font-size 23px
                    display flex


</style>
