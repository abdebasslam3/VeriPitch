import { NextResponse } from 'next/server';
import Whop from '@whop/sdk';

/**
 * API Route to handle Whop OAuth callback.
 * This route exchanges the authorization code for an access token.
 */
export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  if (!code) {
    return NextResponse.json({ error: 'Authorization code missing' }, { status: 400 });
  }

  try {
    const whop = new Whop({ apiKey: process.env.WHOP_API_KEY });

    // 1. Exchange code for access tokens
    // Note: The actual SDK method name might vary based on version,
    // but the logic follows OAuth 2.1 standards.
    const tokenResponse = await whop.oauth.getAccessToken({
      code,
      redirectUri: `${request.nextUrl.origin}/api/auth/whop`,
    });

    // 2. Use token to get user info (optional but recommended)
    // const user = await whop.users.me({ accessToken: tokenResponse.access_token });

    // 3. Redirect user back to dashboard or home with success
    const dashboardUrl = new URL('/dashboard', request.nextUrl.origin);
    dashboardUrl.searchParams.set('auth', 'success');

    return NextResponse.redirect(dashboardUrl);

  } catch (error) {
    console.error('Whop OAuth Error:', error);
    return NextResponse.json({
      error: 'Authentication failed',
      message: error.message
    }, { status: 500 });
  }
}
