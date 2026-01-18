const SHARED_COMPONENTS = {
    header: `
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-card/95 backdrop-blur-md border-b border-slate-200">
        <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-12 py-3 sm:py-4">
            <div class="flex items-center justify-between gap-2">
                <!-- Left: Mobile menu + Logo -->
                <div class="flex items-center gap-2">
                    <!-- Mobile menu button -->
                    <button id="mobile-menu-open" class="lg:hidden p-2 hover:bg-slate-100 rounded-lg transition-colors" aria-label="Open Menu">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="4" x2="20" y1="12" y2="12" />
                            <line x1="4" x2="20" y1="6" y2="6" />
                            <line x1="4" x2="20" y1="18" y2="18" />
                        </svg>
                    </button>

                    <!-- Logo -->
                    <a href="/" class="flex items-center gap-1 sm:gap-1.5 shrink-0">
                        <span class="text-2xl sm:text-3xl">🐕</span>
                        <div class="flex flex-col shrink-0 overflow-hidden whitespace-nowrap">
                            <span id="brand-name" class="text-lg font-extrabold sm:text-lg lg:text-2xl lg:font-bold text-primary font-heading leading-none"></span>
                            <span class="text-[8px] sm:text-[9px] lg:text-[10px] text-slate-500 hidden sm:block">Natural and Nutritious</span>
                        </div>
                    </a>
                </div>
                
                <!-- Center: Search Bar (Desktop only) -->
                <div class="hidden lg:flex flex-1 justify-center">
                    <div class="relative w-full max-w-md">
                        <svg class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
                            xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="11" cy="11" r="8" />
                            <path d="m21 21-4.3-4.3" />
                        </svg>
                        <form action="/search/" method="GET" class="w-full flex">
                            <input type="text" name="q" placeholder="Search products..."
                                class="flex-1 pl-11 pr-4 py-2.5 rounded-l-full border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm">
                            <button type="submit" class="px-4 py-2.5 bg-primary text-white rounded-r-full hover:bg-primary-dark transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="11" cy="11" r="8" />
                                    <path d="m21 21-4.3-4.3" />
                                </svg>
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Right: Icons -->
                <div class="flex items-center gap-0.5 sm:gap-2">
                    <!-- Mobile Search Button -->
                    <!-- Removed - search moved to separate row on mobile -->
                    
                    <!-- Notifications Bell (Orders + Messages) -->
                    <div class="relative">
                        <button id="notification-btn" class="p-2 sm:p-2.5 hover:bg-slate-100 rounded-full transition-colors text-slate-700 relative group" aria-label="Notifications">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
                                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                            </svg>
                            <span id="notification-badge" class="absolute top-0.5 right-0.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center opacity-0 transition-opacity">0</span>
                        </button>
                        
                        <!-- Notification Dropdown -->
                        <div id="notification-dropdown" class="absolute right-0 top-full mt-2 w-[420px] bg-white rounded-xl shadow-lg border border-slate-200 z-50 hidden">
                            <div class="px-8 py-5 border-b border-slate-100 flex items-center justify-between gap-8">
                                <h3 class="font-semibold text-slate-900 text-base">Notifications</h3>
                                <button id="clear-all-btn" class="text-sm text-primary hover:text-primary-dark font-medium whitespace-nowrap">Clear All</button>
                            </div>
                            <div id="notification-list" class="max-h-64 overflow-y-auto">
                                <div class="p-4 text-center text-slate-500 text-sm">No new notifications</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Wishlist -->
                    <a href="/wishlist/" class="p-2 sm:p-2.5 hover:bg-slate-100 rounded-full transition-colors text-slate-700 relative group" aria-label="Wishlist">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                        </svg>
                        <span id="wishlist-badge" class="absolute top-0.5 right-0.5 w-4 h-4 bg-primary text-white text-[9px] font-bold rounded-full flex items-center justify-center opacity-0 transition-opacity">0</span>
                    </a>
                    
                    <!-- Profile -->
                    <a href="/profile/" class="hidden lg:block p-2 sm:p-2.5 hover:bg-slate-100 rounded-full transition-colors text-slate-700" aria-label="Profile">
                         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    </a>

                    <!-- Cart -->
                    <a href="/cart/" class="p-2 sm:p-2.5 hover:bg-slate-100 rounded-full transition-colors relative group" aria-label="Cart">
                        <svg class="text-slate-700 group-hover:text-primary transition-colors"
                            xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="8" cy="21" r="1" />
                            <circle cx="19" cy="21" r="1" />
                            <path
                                d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" />
                        </svg>
                        <span id="cart-badge" class="absolute top-0.5 right-0.5 w-4 h-4 bg-primary text-white text-[9px] font-bold rounded-full flex items-center justify-center opacity-0 transition-opacity">0</span>
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Search Bar and Profile Row - Mobile Only -->
        <div class="lg:hidden bg-white border-t border-slate-100">
            <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-12 py-3">
                <div class="flex items-center gap-4">
                    <!-- Search Bar - 3/4 width -->
                    <div class="flex-1 max-w-3xl">
                        <div class="relative w-full">
                            <svg class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
                                xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="11" cy="11" r="8" />
                                <path d="m21 21-4.3-4.3" />
                            </svg>
                            <form action="/search/" method="GET" class="w-full flex">
                                <input type="text" name="q" placeholder="Search products..."
                                    class="flex-1 pl-11 pr-4 py-2.5 rounded-l-full border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm">
                                <button type="submit" class="px-4 py-2.5 bg-primary text-white rounded-r-full hover:bg-primary-dark transition-colors">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <circle cx="11" cy="11" r="8" />
                                        <path d="m21 21-4.3-4.3" />
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </div>
                    
                    <!-- Profile - Mobile Only -->
                    <a href="/profile/" class="lg:hidden p-2 sm:p-2.5 hover:bg-slate-100 rounded-full transition-colors text-slate-700" aria-label="Profile">
                         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    </a>
                </div>
            </div>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden lg:block border-t border-slate-100 bg-white">
            <div class="max-w-[1440px] mx-auto px-12">
                <ul class="flex items-center justify-center gap-10 py-3">
                    <li><a href="/shop/"
                            class="flex items-center gap-1 text-sm font-semibold text-slate-700 hover:text-primary transition-colors py-2 group">
                            Shop
                            <svg class="group-hover:translate-y-0.5 transition-transform" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round">
                                <path d="m6 9 6 6 6-6" />
                            </svg></a></li>
                    <li><a href="/shop/?category=dog-food"
                            class="text-sm font-semibold text-slate-700 hover:text-primary transition-colors py-2">Dog
                            Food</a></li>
                    <li><a href="/shop/?category=cat-food"
                            class="text-sm font-semibold text-slate-700 hover:text-primary transition-colors py-2">Cat
                            Food</a></li>
                    <li><a href="/shop/?category=accessories"
                            class="text-sm font-semibold text-slate-700 hover:text-primary transition-colors py-2">Accessories</a>
                    </li>
                    <li><a href="/about/"
                            class="text-sm font-semibold text-slate-700 hover:text-primary transition-colors py-2">About</a>
                    </li>
                    <li><a href="/blog/"
                            class="text-sm font-semibold text-slate-700 hover:text-primary transition-colors py-2">Blog</a>
                    </li>
                </ul>
            </div>
        </nav>
    </header>

    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu" class="fixed inset-0 z-[100] bg-black/50 invisible transition-all duration-300 lg:hidden">
        <div class="absolute left-0 top-0 h-full w-[240px] bg-white shadow-2xl -translate-x-full transition-transform duration-300 ease-out flex flex-col">
            <div class="p-4 border-b border-slate-100 flex items-center justify-between">
                <span class="text-lg font-bold text-primary font-heading">Menu</span>
                <button id="mobile-menu-close" class="p-2 hover:bg-slate-100 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            </div>
            <nav class="flex-1 overflow-y-auto p-4">
                <!-- Mobile Search Bar -->
                <div id="mobile-search-bar" class="mb-6 hidden">
                    <div class="relative">
                        <svg class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                            xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="11" cy="11" r="8" />
                            <path d="m21 21-4.3-4.3" />
                        </svg>
                        <form action="/search/" method="GET" class="w-full">
                            <input type="text" name="q" placeholder="Search products..."
                                class="w-full pl-10 pr-4 py-2.5 rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm">
                        </form>
                    </div>
                </div>
                
                <ul class="space-y-4">
                    <li><a href="/" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">Home</a></li>
                    <li><a href="/shop/" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">Shop All</a></li>
                    <li><a href="/shop/?category=dog-food" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">Dog Food</a></li>
                    <li><a href="/shop/?category=cat-food" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">Cat Food</a></li>
                    <li><a href="/shop/?category=accessories" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">Accessories</a></li>
                    <li><a href="/about/" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">About Us</a></li>
                    <li><a href="/blog/" class="block text-base font-semibold text-slate-800 hover:text-primary py-2">Blog</a></li>
                </ul>
            </nav>
            <div class="p-4 border-t border-slate-100 bg-slate-50">
                <div id="auth-section">
                    <!-- This will be populated by JavaScript based on user authentication -->
                </div>
                <div class="mt-4 pt-4 border-t border-slate-200 text-center">
                    <span class="text-lg font-bold text-primary font-heading">FURFEAST CO.</span>
                </div>
            </div>
        </div>
    </div>
    `,
    footer: `
    <footer class="bg-slate-900 text-slate-300 py-8 sm:py-16">
        <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-12">
            <!-- Mobile: 3 columns side by side -->
            <div class="grid grid-cols-3 md:grid-cols-4 gap-4 md:gap-12 mb-8 sm:mb-16 text-center md:text-left">
                <!-- Brand - Hidden on mobile, shown on desktop -->
                <div class="hidden md:block md:col-span-1">
                    <div class="flex items-center justify-center md:justify-start gap-2 mb-6">
                        <span class="text-3xl">🐕</span>
                        <span class="text-2xl font-bold text-white font-heading">FURFEAST CO.</span>
                    </div>
                    <p class="mb-8 max-w-sm mx-auto md:mx-0 text-slate-400 text-sm leading-relaxed">Premium pet nutrition and accessories delivered to your door. Because your pets deserve the best, naturally.</p>
                    <div class="flex justify-center md:justify-start gap-4">
                        <a href="https://www.facebook.com/share/1ChcEySvre/?mibextid=wwXIfr" target="_blank" class="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
                        </a>
                        <a href="https://www.instagram.com/furfeast.co?igsh=MTN4eXk4YzRzcHdhdA%3D%3D&utm_source=qr" target="_blank" class="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
                        </a>
                        <a href="https://www.tiktok.com/@furfeast.co?_r=1&_t=ZS-931i5Beq7LU" target="_blank" class="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
                        </a>
                        <a href="tel:+61450233255" class="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                        </a>
                    </div>
                </div>

                <!-- Shop -->
                <div>
                    <h4 class="text-white font-bold mb-3 md:mb-6 text-sm md:text-base">Shop</h4>
                    <ul class="space-y-1 md:space-y-4">
                        <li><a href="/shop/?category=dog-food" class="text-xs md:text-sm hover:text-primary transition-colors">Dog Food</a></li>
                        <li><a href="/shop/?category=cat-food" class="text-xs md:text-sm hover:text-primary transition-colors">Cat Food</a></li>
                        <li><a href="/shop/?category=accessories" class="text-xs md:text-sm hover:text-primary transition-colors">Accessories</a></li>
                    </ul>
                </div>

                <!-- Company -->
                <div>
                    <h4 class="text-white font-bold mb-3 md:mb-6 text-sm md:text-base">Company</h4>
                    <ul class="space-y-1 md:space-y-4">
                        <li><a href="/about/" class="text-xs md:text-sm hover:text-primary transition-colors">About Us</a></li>
                        <li><a href="/blog/" class="text-xs md:text-sm hover:text-primary transition-colors">Blog</a></li>
                        <li><a href="/contact/" class="text-xs md:text-sm hover:text-primary transition-colors">Contact Us</a></li>
                    </ul>
                </div>

                <!-- Support -->
                <div>
                    <h4 class="text-white font-bold mb-3 md:mb-6 text-sm md:text-base">Support</h4>
                    <ul class="space-y-1 md:space-y-4">
                        <li><a href="/shipping/" class="text-xs md:text-sm hover:text-primary transition-colors">Shipping Policy</a></li>
                        <li><a href="/refund/" class="text-xs md:text-sm hover:text-primary transition-colors">Returns</a></li>
                        <li><a href="/terms/" class="text-xs md:text-sm hover:text-primary transition-colors">Terms Conditions</a></li>
                    </ul>
                </div>
            </div>

            <!-- Mobile Brand Section -->
            <div class="md:hidden text-center mb-8">
                <div class="flex items-center justify-center gap-2 mb-4">
                    <span class="text-2xl">🐕</span>
                    <span class="text-xl font-bold text-white font-heading">FURFEAST CO.</span>
                </div>
                <div class="flex justify-center gap-3">
                    <a href="https://www.facebook.com/share/1ChcEySvre/?mibextid=wwXIfr" target="_blank" class="w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
                    </a>
                    <a href="https://www.instagram.com/furfeast.co?igsh=MTN4eXk4YzRzcHdhdA%3D%3D&utm_source=qr" target="_blank" class="w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
                    </a>
                    <a href="https://www.tiktok.com/@furfeast.co?_r=1&_t=ZS-931i5Beq7LU" target="_blank" class="w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
                    </a>
                    <a href="tel:+61450233255" class="w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    </a>
                </div>
            </div>

            <div class="pt-6 border-t border-slate-800 text-center text-xs md:text-sm">
                <p>&copy; 2025 FURFEAST CO. All rights reserved.</p>
            </div>
        </div>
    </footer>
    `
};

function injectLayout() {
    const headerPlaceholder = document.getElementById('shopify-section-header');
    const footerPlaceholder = document.getElementById('shopify-section-footer');

    if (headerPlaceholder) {
        // Read data attributes for dynamic counts
        const cartCount = headerPlaceholder.getAttribute('data-cart-count') || 0;
        const wishlistCount = headerPlaceholder.getAttribute('data-wishlist-count') || 0;

        // Use innerHTML for static template content (safe as it's not user-controlled)
        headerPlaceholder.innerHTML = SHARED_COMPONENTS.header;

        // Update badges efficiently
        requestAnimationFrame(() => {
            const cartBadge = document.getElementById('cart-badge');
            const wishlistBadge = document.getElementById('wishlist-badge');
            const notificationBadge = document.getElementById('notification-badge');
            const notificationCount = headerPlaceholder.getAttribute('data-notification-count') || 0;

            if (cartBadge) {
                cartBadge.textContent = cartCount;
                cartBadge.classList.toggle('opacity-0', parseInt(cartCount) <= 0);
                cartBadge.classList.toggle('opacity-100', parseInt(cartCount) > 0);
            }

            if (wishlistBadge) {
                wishlistBadge.textContent = wishlistCount;
                wishlistBadge.classList.toggle('opacity-0', parseInt(wishlistCount) <= 0);
                wishlistBadge.classList.toggle('opacity-100', parseInt(wishlistCount) > 0);
            }
            
            if (notificationBadge) {
                notificationBadge.textContent = notificationCount;
                notificationBadge.classList.toggle('opacity-0', parseInt(notificationCount) <= 0);
                notificationBadge.classList.toggle('opacity-100', parseInt(notificationCount) > 0);
            }
        });
        
        // Notification functionality (orders + messages)
        const notificationBtn = document.getElementById('notification-btn');
        const notificationDropdown = document.getElementById('notification-dropdown');
        const clearAllBtn = document.getElementById('clear-all-btn');
        
        if (notificationBtn && notificationDropdown) {
            notificationBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                notificationDropdown.classList.toggle('hidden');
                if (!notificationDropdown.classList.contains('hidden')) {
                    loadNotifications();
                }
            });
            
            document.addEventListener('click', () => {
                notificationDropdown.classList.add('hidden');
            });
            
            notificationDropdown.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
        
        if (clearAllBtn) {
            clearAllBtn.removeEventListener('click', clearAllNotifications);
            clearAllBtn.addEventListener('click', clearAllNotifications);
        }

        // Optimized Mobile Menu Logic with event delegation
        const mobileMenu = document.getElementById('mobile-menu');
        const openBtn = document.getElementById('mobile-menu-open');
        const closeBtn = document.getElementById('mobile-menu-close');
        const mobileSearchBtn = document.getElementById('mobile-search-btn');
        const mobileSearchBar = document.getElementById('mobile-search-bar');

        if (mobileMenu && openBtn && closeBtn) {
            const menuContent = mobileMenu.firstElementChild;

            const openMenu = () => {
                mobileMenu.classList.remove('invisible');
                requestAnimationFrame(() => menuContent.classList.remove('-translate-x-full'));
                document.body.style.overflow = 'hidden';
            };

            const closeMenu = () => {
                menuContent.classList.add('-translate-x-full');
                setTimeout(() => {
                    mobileMenu.classList.add('invisible');
                    document.body.style.overflow = '';
                    if (mobileSearchBar) {
                        mobileSearchBar.classList.add('hidden');
                    }
                }, 300);
            };

            openBtn.addEventListener('click', openMenu, { passive: true });
            closeBtn.addEventListener('click', closeMenu, { passive: true });
            mobileMenu.addEventListener('click', (e) => {
                if (e.target === mobileMenu) closeMenu();
            }, { passive: true });
        }

        // Optimized Mobile Search Button Logic
        if (mobileSearchBtn && mobileSearchBar) {
            mobileSearchBtn.addEventListener('click', () => {
                if (mobileMenu && !mobileMenu.classList.contains('invisible')) {
                    mobileSearchBar.classList.toggle('hidden');
                } else {
                    mobileMenu.classList.remove('invisible');
                    const menuContent = mobileMenu.firstElementChild;
                    requestAnimationFrame(() => {
                        menuContent.classList.remove('-translate-x-full');
                        mobileSearchBar.classList.remove('hidden');
                        const searchInput = mobileSearchBar.querySelector('input');
                        if (searchInput) {
                            setTimeout(() => searchInput.focus(), 100);
                        }
                    });
                    document.body.style.overflow = 'hidden';
                }
            }, { passive: true });
        }

        // Optimized active link highlighting
        requestAnimationFrame(() => {
            const currentPath = window.location.pathname;
            const navLinks = headerPlaceholder.querySelectorAll('nav a');
            navLinks.forEach(link => {
                const linkHref = link.getAttribute('href');
                if (linkHref === currentPath || (currentPath === '/' && linkHref === '/')) {
                    link.classList.add('text-primary');
                    link.classList.remove('text-slate-700');
                    if (link.parentElement.tagName === 'LI' && !link.querySelector('svg')) {
                        link.classList.add('border-b-2', 'border-primary');
                    }
                }
            });
        });

        // Update authentication section safely
        const authSection = document.getElementById('auth-section');
        if (authSection) {
            const isAuthenticated = document.body.dataset.authenticated === 'true';
            
            // Clear existing content
            authSection.textContent = '';
            
            if (isAuthenticated) {
                // Create authenticated user section
                const containerDiv = document.createElement('div');
                containerDiv.className = 'space-y-2';
                
                // Profile link
                const profileLink = document.createElement('a');
                profileLink.href = '/profile/';
                profileLink.className = 'block w-full text-center py-2 px-4 bg-slate-200 text-slate-800 rounded-lg font-semibold hover:bg-slate-300 transition-colors text-sm';
                profileLink.textContent = 'View Profile';
                
                // Logout link
                const logoutLink = document.createElement('a');
                logoutLink.href = '/logout/';
                logoutLink.className = 'block w-full text-center py-2 px-4 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition-colors text-sm';
                logoutLink.textContent = 'Sign Out';
                
                containerDiv.appendChild(profileLink);
                containerDiv.appendChild(logoutLink);
                authSection.appendChild(containerDiv);
            } else {
                // Create sign in link
                const signInLink = document.createElement('a');
                signInLink.href = '/login/';
                signInLink.className = 'block w-full text-center py-2 px-4 bg-primary text-white rounded-lg font-semibold hover:bg-primary-dark transition-colors text-sm';
                signInLink.textContent = 'Sign In';
                authSection.appendChild(signInLink);
            }
        }

        // Optimized brand name display
        const brandElement = document.getElementById('brand-name');
        if (brandElement) {
            brandElement.textContent = "FURFEAST CO.";
        }
    }

    if (footerPlaceholder) {
        footerPlaceholder.innerHTML = SHARED_COMPONENTS.footer;
    }
}

// Use more efficient DOM ready detection
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectLayout);
} else {
    injectLayout();
}

// Helper function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Notification functions (all types)
function loadNotifications() {
    fetch(`/api/notifications/?t=${Date.now()}`, {
        cache: 'no-store',
        headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
    })
        .then(response => response.json())
        .then(data => {
            const notificationList = document.getElementById('notification-list');
            notificationList.textContent = '';
            
            if (data.notifications && data.notifications.length > 0) {
                data.notifications.forEach(notification => {
                    const notificationDiv = document.createElement('div');
                    const isMessage = notification.notification_type === 'message';
                    notificationDiv.className = `p-4 border-b border-slate-100 hover:bg-slate-50 cursor-pointer ${notification.is_read ? 'opacity-60' : ''} ${isMessage ? 'border-l-4 border-l-blue-500' : 'border-l-4 border-l-green-500'}`;
                    notificationDiv.addEventListener('click', () => markAsRead(notification.id, notification.link));
                    
                    const titleDiv = document.createElement('div');
                    titleDiv.className = `font-medium text-slate-900 text-sm ${notification.is_read ? '' : 'font-bold'}`;
                    titleDiv.textContent = (isMessage ? '💬 ' : '📦 ') + notification.title;
                    
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'text-slate-600 text-xs mt-1';
                    messageDiv.textContent = notification.message;
                    
                    const timeDiv = document.createElement('div');
                    timeDiv.className = 'text-slate-400 text-xs mt-2';
                    timeDiv.textContent = notification.created_at;
                    
                    notificationDiv.appendChild(titleDiv);
                    notificationDiv.appendChild(messageDiv);
                    notificationDiv.appendChild(timeDiv);
                    notificationList.appendChild(notificationDiv);
                });
            } else {
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'p-4 text-center text-slate-500 text-sm';
                emptyDiv.textContent = 'No notifications';
                notificationList.appendChild(emptyDiv);
            }
        })
        .catch(error => console.error('Error loading notifications:', error));
}

function markAsRead(notificationId, link) {
    fetch(`/api/notifications/${notificationId}/read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotifications();
            updateNotificationBadge();
            if (link) {
                window.location.href = link;
            }
        }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

let notificationInterval = null;

function clearAllNotifications() {
    const clearBtn = document.getElementById('clear-all-btn');
    if (clearBtn && clearBtn.disabled) return;
    if (clearBtn) clearBtn.disabled = true;
    
    // Stop auto-refresh temporarily
    if (notificationInterval) {
        clearInterval(notificationInterval);
    }
    
    // Make API call to delete from database FIRST
    fetch('/api/notifications/clear/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(() => {
        // After successful deletion, update UI
        const badge = document.getElementById('notification-badge');
        if (badge) {
            badge.textContent = '0';
            badge.classList.add('opacity-0');
            badge.classList.remove('opacity-100');
        }
        
        const notificationList = document.getElementById('notification-list');
        if (notificationList) {
            notificationList.innerHTML = '<div class="p-4 text-center text-slate-500 text-sm">No notifications</div>';
        }
        
        const dropdown = document.getElementById('notification-dropdown');
        if (dropdown) dropdown.classList.add('hidden');
        
        // Restart auto-refresh
        notificationInterval = setInterval(updateNotificationBadge, 3000);
    })
    .catch(error => {
        console.error('Clear error:', error);
        // Restart auto-refresh even on error
        notificationInterval = setInterval(updateNotificationBadge, 3000);
    })
    .finally(() => {
        if (clearBtn) clearBtn.disabled = false;
    });
}

function updateNotificationBadge() {
    fetch(`/api/notifications/?t=${Date.now()}`, {
        cache: 'no-store',
        headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
    })
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notification-badge');
            if (badge) {
                badge.textContent = data.count || 0;
                badge.classList.toggle('opacity-0', (data.count || 0) <= 0);
                badge.classList.toggle('opacity-100', (data.count || 0) > 0);
            }
        })
        .catch(error => console.error('Error updating notification badge:', error));
}

// Auto-update badge every 3 seconds for real-time updates
notificationInterval = setInterval(updateNotificationBadge, 3000);

// Update badge on page load
document.addEventListener('DOMContentLoaded', updateNotificationBadge);
